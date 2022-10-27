import pandas as pd
import numpy as np


def init():
    global development
    development = False

    global dataset
    dataset = None


def init_dev():
    global development
    development = True
    
    with open("dataset.xlsx", "rb") as file:
        file_content = file.read()

    df = pd.read_excel(file_content)

    global dataset
    dataset = df

    dataset.at[0, "Age"] = 2
    dataset.at[5, "Age"] = 74
    dataset.at[0, "Education"] = np.nan
    dataset.at[0, "Department"] = np.nan

    global round_to
    round_to = 4
