import pandas as pd
import numpy as np


def init():
    global development
    development = False

    global dataset
    dataset = None

    global round_to
    round_to = 4


def init_dev():
    global development
    development = True
    
    with open("dataset.xlsx", "rb") as file:
        file_content = file.read()

    df = pd.read_excel(file_content)

    global dataset
    dataset = df

    global round_to
    round_to = 4
