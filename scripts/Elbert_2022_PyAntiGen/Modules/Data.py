import pandas as pd
import os


def load_data(data_name, data_path):
    # Load experimental data from data folder
    data_path = os.path.join(data_path, data_name)
    df = pd.read_csv(data_path)  # utf-8-sig strips BOM if present
    return df



def load_experiment1_data(data_path):
    experiment_path = os.path.join(data_path, 'Elbert_2022_all_data.csv')
    df = pd.read_csv(experiment_path)
    return df

