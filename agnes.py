from time import time

import pandas as pd
import numpy as np

from dm.agnes.agnes import Agnes
from dm.agnes.distances import minimal_distance, maximal_distance, mean_distance, similarity
from dm.agnes.metrics import intraclusters_distance, interclusters_distance
from dm.agnes.configuration import Configuration

def random_points(dataset, size):
    if not dataset:
        return []
    
    random_dataset = []
    length_dataset = len(dataset)
    indicies = {}

    count = 0
    while True:
        if count == size:
            break

        index = np.random.randint(0, length_dataset)
        if indicies.get(index, False):
            continue
        
        indicies.update({index: True})
        random_dataset.append(dataset[index])
        count += 1
    
    return random_dataset

if __name__ == "__main__":
    df = pd.read_excel("Dataset1_pretraitement_complet.xlsx")
    dataset = list(df.itertuples(index=False, name=None))

    m = len(dataset)

    pourecentage = 20
    m_test = np.ceil(pourecentage / 100 * m).astype(int)
    
    random_dataset = random_points(dataset, m_test)

    configuration = Configuration(
        dataset=random_dataset, 
        c2c_distance_functions=["minimal_distance", "maximal_distance", "mean_distance"],
        # centroid linkage cannot be applyied here because we do not know how to compute the centroid of cluster
    )

    c2c_distance_functions = {
        "minimal_distance": minimal_distance,
        "maximal_distance": maximal_distance,
        "mean_distance": mean_distance,
    }

    possible_combinations = configuration.possible_combinations()

    n_possible_combinations = len(possible_combinations)
    print(f"n_possible_combinations = {n_possible_combinations}")

    with open("agnes_evaluation.csv", "w") as file:
        file.write("cluster to cluster function, intra-clusters distance (number of clusters is 2), inter-clusters mean distance (number of clusters is 2), clustering time\n")

    for index, (dataset, c2c_distance_function) in enumerate(possible_combinations, start=1):
        print("-"* 100)
        print(f"combination {index}:")

        algorithm = Agnes(c2c_distance_function=c2c_distance_functions[c2c_distance_function](distance_function=similarity))
        print(f"\tc2c distance function = {c2c_distance_function}\n")
        
        start = time()
        history = algorithm(dataset=dataset)
        finish = time()

        duration = round(finish - start)

        print("*" * 100)
        print(f"done clustering in {duration} seconds")

        # measures - where number of clusters is 2
        clusters = history[2]
        measure_1 = intraclusters_distance(clusters, similarity)
        measure_2 = interclusters_distance(clusters, c2c_distance_functions[c2c_distance_function](distance_function=similarity))
        measure_3 = duration
        
        # print("*" * 100)
        # print(f"measure 1 (intra-clusters distance for clusters list of size 2): {measure_1}")
        # print(f"measure 2 (inter-clusters distance for clusters list of size 2): {measure_2}")
        # print(f"measure 3 (duration of clustering): {measure_3}")

        with open("agnes_evaluation.csv", "a") as file:
            print("writing to the file")
            file.write(f"{c2c_distance_function}, {measure_1}, {measure_2}, {measure_3}\n")

        print("*" * 100)

        # quit = input("want to quit? [y/(N)]: ")

        # if quit.lower() == "y":
        #     break