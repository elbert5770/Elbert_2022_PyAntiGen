import numpy as np
from typing import List, Union, Tuple

def generate_events():
    events = '' 
    return events

def event1(df,Q_CSF,V_SP3_0,V_LP,t_CSFdraw):
    events = ''

    

    event_line = f"at (time >= 0.0 ): Q_Leak = 15.0"
    events += event_line + "\n"

    event_line = f"at (time >= 3.0 ): Q_Leak = 0.0"
    events += event_line + "\n"
 
    event_line = f"at (time > 20.0): Q_Leak = Q_CSF-Q_SN"
    events += event_line + "\n"

   
    event_line = f"at (time >= 30.0): Q_Leak = 0.0"
    events += event_line + "\n"

    
    event_line = f"at (time >= 48.0): Q_Leak = 0.0"
    events += event_line + "\n"

    events += hourly_events() + "\n"
    events += construct_volume_interpolation(Q_CSF,V_SP3_0,V_LP,t_CSFdraw) + "\n"
    events += construct_f13C6Leu_interpolation(df) + "\n"
    print(events)
    return events

def hourly_events():
    events = ''
    for i in range(0, 48):
        event_line = f"at (time >= {i}): Q_SN = 0.0, Q_LP = Q_CSF, Q_refill = Q_CSF - V_LP/t_CSFdraw"
        events += event_line + "\n"
        event_line = f"at (time >= {i} + t_CSFdraw):  Q_refill = Q_CSF"
        events += event_line + "\n"
        event_line = f"at (time >= {i} + V_LP/Q_CSF): Q_SN = f_SN*Q_CSF, Q_LP = Q_Leak, Q_refill = 0"
        events += event_line + "\n"
    return events

def construct_volume_interpolation(Q_CSF,V_SP3_0,V_LP,t_CSFdraw):
    
    slope1 = Q_CSF - V_LP/t_CSFdraw
    time_points = []
    data_points = []
    for i in range(0,48):
        time_points.append(i)
        time_points.append(i + t_CSFdraw)
        time_points.append(i + V_LP/Q_CSF)
        data_points.append(V_SP3_0)
        data_points.append(V_SP3_0 + slope1*t_CSFdraw)
        data_points.append(V_SP3_0)

    return generate_antimony_piecewise(time_points, data_points, data_name="V_SP3", default_before=V_SP3_0, default_after=V_SP3_0)

def construct_f13C6Leu_interpolation(df):
    times = df["time"].values
    data = df["PlasmaLeu"].values
    
    mask = ~(np.isnan(times) | np.isnan(data))
    times = times[mask]
    data = data[mask]

    return generate_antimony_piecewise(times, data, data_name="f_13C6Leu", default_before=0, default_after=0)

def generate_antimony_piecewise(
    times: Union[List[float], np.ndarray],
    data: Union[List[float], np.ndarray],
    data_name: str = "data",
    time_var: str = "time",
    default_before: Union[float, None] = None,
    default_after: Union[float, None] = None
) -> str:
    """
    Generate an Antimony piecewise function with linear interpolation.
    
    Parameters
    ----------
    times : array-like
        Vector of time points (must be sorted in ascending order)
    data : array-like
        Vector of data values corresponding to each time point
    data_name : str
        Name of the data variable in Antimony output (default: "data")
    time_var : str
        Name of the time variable in Antimony output (default: "time")
    default_before : float or None
        Value to use for times before the first point. If None, defaults to 0.0.
    default_after : float or None
        Value to use for times after the last point. If None, defaults to 0.0.
    
    Returns
    -------
    str
        Antimony piecewise function definition
    """
    times = np.array(times)
    data = np.array(data)
    
    # Validate inputs
    if len(times) != len(data):
        raise ValueError("times and data must have the same length")
    if len(times) < 2:
        raise ValueError("At least 2 points are required for interpolation")
    
    # Sort by time to ensure proper ordering
    sort_idx = np.argsort(times)
    times = times[sort_idx]
    data = data[sort_idx]
    
    # Set defaults to 0.0 for times outside the data range
    if default_before is None:
        default_before = 0.0
    if default_after is None:
        default_after = 0.0
    
    # Build piecewise conditions and expressions
    pieces = []
    
    # Handle times before first point
    pieces.append(format_number(default_before))
    pieces.append(f"{time_var} < {format_number(times[0])}")
    
    # Generate linear interpolation for each interval
    for i in range(len(times) - 1):
        t_i = times[i]
        t_next = times[i + 1]
        v_i = data[i]
        v_next = data[i + 1]
        
        # Skip if times are equal (would cause division by zero)
        if abs(t_next - t_i) < 1e-10:
            continue
        
        # Linear interpolation formula: v = v_i + (v_next - v_i) * (t - t_i) / (t_next - t_i)
        # For Antimony, we'll use: (v_i + (v_next - v_i) * (time_var - t_i) / (t_next - t_i))
        
        # Build the interpolation expression
        if abs(v_next - v_i) < 1e-10:
            # Constant value (no interpolation needed)
            interp_expr = format_number(v_i)
        else:
            # Linear interpolation: v_i + slope * (time_var - t_i) / dt
            slope = v_next - v_i
            dt = t_next - t_i
            v_i_str = format_number(v_i)
            slope_str = format_number(slope)
            t_i_str = format_number(t_i)
            dt_str = format_number(dt)
            interp_expr = f"({v_i_str} + ({slope_str} * ({time_var} - {t_i_str})) / {dt_str})"
        
        pieces.append(interp_expr)
        pieces.append(f"{time_var} < {format_number(t_next)}")
    
    # Handle times after last point
    pieces.append(format_number(default_after))
    pieces.append(f"{time_var} > {format_number(times[-1])}")
    
    # Join pieces into Antimony piecewise function
    piecewise_str = ", ".join(pieces)
    result = f"{data_name} := piecewise({piecewise_str})"
    
    return result




def format_number(num: float, precision: int = 15) -> str:
    """
    Format a number for Antimony output, removing unnecessary trailing zeros.
    
    Parameters
    ----------
    num : float
        Number to format
    precision : int
        Maximum number of decimal places (default: 15)
    
    Returns
    -------
    str
        Formatted number string
    """
    # Use g format to remove trailing zeros, but limit precision
    formatted = f"{num:.{precision}g}"
    # Remove trailing decimal point if present
    if formatted.endswith('.'):
        formatted = formatted[:-1]
    return formatted
        


