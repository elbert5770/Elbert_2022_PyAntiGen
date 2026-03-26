# Elbert_2022_PyAntiGen

This repository contains the implementation of the Elbert 2022 model, utilizing the PyAntiGen framework for modular model generation, simulation, and optimization.

## Prerequisites

**Important:** This repository requires the **PyAntiGen** framework to function. 
You must clone the PyAntiGen repository (https://github.com/Elbert-Lab/PyAntiGen) and ensure its modules are accessible in your Python environment (e.g., by adding its path to your `PYTHONPATH` or installing it, depending on PyAntiGen's setup instructions) before running any of the scripts here.

## Directory Structure

*   **`scripts/Elbert_2022_PyAntiGen/`**: The main execution scripts for this model.
    *   `Elbert_2022_PyAntiGen_generate.py`: Generates the Antimony/SBML models based on PyAntiGen modules.
    *   `Elbert_2022_PyAntiGen_run.py`: Runs baseline simulations.
    *   `Elbert_2022_PyAntiGen_optimize.py`: Script for parameter estimation/optimization.
    *   `Modules/`: Contains the specific biological module definitions for the Elbert 2022 model.
*   **`modules/`**: General PyAntiGen modules.
*   **`antimony_models/`**: Stores generated Antimony (`.txt`) model files.
*   **`SBML_models/`**: Stores generated SBML (`.xml`) model files.
*   **`results/`**: Output directory for simulation results, plots, and optimized parameters.
*   **`data/`**: Datasets used for validation or parameter fitting.
*   **`pyantigen_settings.json`**: Global project settings.

## Usage

1. Clone PyAntiGen and set it up in your environment.
2. Clone this repository.
3. Open a terminal and navigate to this repository's root.
4. Go to `scripts/Elbert_2022_PyAntiGen/` and execute the desired script:
   ```bash
   # Generates the model
   python Elbert_2022_PyAntiGen_generate.py
   
   # Runs a simulation on the generated model
   python Elbert_2022_PyAntiGen_run.py 
   ```

You may also run the Example script to test the framework:
Go to `scripts/Example/` and execute the desired script:
   ```bash
   # Generates the model
   python Example_generate.py
   
   # Runs a simulation on the generated model
   python Example_run.py 
   ```
