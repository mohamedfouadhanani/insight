import pandas as pd
# import numpy as np

import dill

from dm import Decision_tree
from dm import Random_forest
from dm import DT_with_ID3

def init():
    global decision_tree_with_id3_model
    decision_tree_with_id3_model = None
    with open("decision_tree_with_id3.model", "rb") as dill_file:
        decision_tree_with_id3_model = dill.load(dill_file)
    print("done saving decision tree with ID3 model...")

    global decision_tree_model
    with open("decision_tree.model", "rb") as dill_file:
        decision_tree_model = dill.load(dill_file)
    print("done getting decision tree model...")

    global random_forest_model
    with open("random_forest.model", "rb") as dill_file:
        random_forest_model = dill.load(dill_file)
    print("done getting random forest model...")
    
    global development
    development = False

    global dataset
    dataset = None

    global round_to
    round_to = 4


def init_dev():
    global decision_tree_with_id3_model
    decision_tree_with_id3_model = None
    with open("decision_tree_with_id3.model", "rb") as dill_file:
        decision_tree_with_id3_model = dill.load(dill_file)
    print("done saving decision tree with ID3 model...")

    global decision_tree_model
    with open("decision_tree.model", "rb") as dill_file:
        decision_tree_model = dill.load(dill_file)
    print("done getting decision tree model...")

    global random_forest_model
    with open("random_forest.model", "rb") as dill_file:
        random_forest_model = dill.load(dill_file)
    print("done getting random forest model...")

    # global decision_tree_model
    # decision_tree_model = Decision_tree.get_model()
    # print("done getting decision tree model...")

    # global random_forest_model
    # random_forest_model = Random_forest.get_model()
    # print("done getting random forest model...")

    global development
    development = True
    
    with open("dataset.xlsx", "rb") as file:
        file_content = file.read()

    df = pd.read_excel(file_content)

    global dataset
    dataset = df

    global round_to
    round_to = 4

if __name__ == "__main__":
    # decision_tree_model = Decision_tree.get_model()
    # with open("decision_tree.model", "wb") as dill_file:
    #     dill.dump(decision_tree_model, dill_file)
    # print("done saving decision tree model...")

    # random_forest_model = Random_forest.get_model()
    # with open("random_forest.model", "wb") as dill_file:
    #     dill.dump(random_forest_model, dill_file)
    # print("done saving decision tree model...")

    # decision_tree_with_id3_model = DT_with_ID3.get_model()
    # with open("decision_tree_with_id3.model", "wb") as dill_file:
    #     dill.dump(decision_tree_with_id3_model, dill_file)
    # print("done saving decision tree model...")

    # decision_tree_model = None
    # with open("decision_tree.model", "rb") as dill_file:
    #     decision_tree_model = dill.load(dill_file)
    # print("done getting decision tree model...")

    # random_forest_model = None
    # with open("random_forest.model", "rb") as dill_file:
    #     random_forest_model = dill.load(dill_file)
    # print("done getting random forest model...")

    # decision_tree_with_id3_model = None
    # with open("decision_tree_with_id3.model", "rb") as dill_file:
    #     decision_tree_with_id3_model = dill.load(dill_file)
    # print("done saving decision tree model...")

    init_dev()