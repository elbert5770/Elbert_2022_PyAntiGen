import time

def simulate(r):
    r.setIntegrator('cvode')
    r.integrator.absolute_tolerance = 1e-16
    r.integrator.relative_tolerance = 1e-14
    r.integrator.setValue('stiff', True)
    r.integrator.variable_step_size = True
    print(r.integrator)

    observed_species = ['time','f_13C6Leu','[APP_BrainISF]','[AB40_BrainISF]','[AB42_BrainISF]',
    '[C99_BrainISF]','[AB40_SAS]','[AB40_CV]','[AB40_SP3]','[AB42_SAS]','[AB42_CV]','[AB42_SP3]',
    '[AB38_BrainISF]','[AB38_SAS]','[AB38_CV]','[AB38_SP3]','[AB38_13C6Leu_SP3]','[AB40_13C6Leu_SP3]','[AB42_13C6Leu_SP3]',
    'Q_LP','f_13C6Leu','[AB38_13C6Leu_BrainISF]','[AB40_13C6Leu_BrainISF]','[AB42_13C6Leu_BrainISF]',
    'Q_SN','Q_refill','Q_Leak', 'V_SP3','AB40_SP3','AB40_13C6Leu_SP3','[AB40_13C6Leu_CV]','[AB40_13C6Leu_SAS]','[AB40_13C6Leu_SP1]','[AB40_13C6Leu_SP2]','[AB40_13C6Leu_SP3]',
    '[AB40_SP1]','[AB40_SP2]','[AB42_SP1]','[AB42_SP2]','[AB38_SP1]','[AB38_SP2]','AB40_SP2','AB40_13C6Leu_SP2',
    'V_SP2']



    print("Running simulation...")
    t0 = time.perf_counter()

    result0 = r.simulate(-10000, 0, 100, observed_species)
    result1 = r.simulate(0, 48, 5760, observed_species)
    
    elapsed = time.perf_counter() - t0
    print(f"Simulation time: {elapsed:.3f} s")
    print(f"CVODE took {len(result1)} steps.")

    return result1
