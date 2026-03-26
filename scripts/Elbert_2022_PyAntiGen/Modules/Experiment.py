"""Experiment registry: one entry per experiment for run and optimize."""
from .Data import load_experiment1_data
from .Events import event1

EXPERIMENTS = [
    {"id": "1", "event_func": event1, "load_data": load_experiment1_data, "label": "Experiment 1"},

]
