from time import time

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "abc"

import pandas as pd

from dm.dbscan.distances import similarity

from dm.dbscan.dbscan import DBSCAN

from dm.dbscan.metrics import n_clusters, interclusters_distance, intraclusters_distance

from dm.dbscan.distances import minimal_distance

from dm.dbscan.configuration import Configuration

if __name__ == "__main__":
    df = pd.read_excel("Dataset1_pretraitement_complet.xlsx")
    dataset = list(df.itertuples(index=False, name=None))

    configuration = Configuration(
        dataset=dataset, 
        p2p_distance_functions=["similarity"],
        minimum_points=[1, 2, 3, 4, 5],
        epsilons=[1, 2, 3]
    )
    
    p2p_distance_functions = {
        "similarity": similarity
    }

    possible_combinations = configuration.possible_combinations()

    n_possible_combinations = len(possible_combinations)
    print(f"n_possible_combinations = {n_possible_combinations}")

    with open("dbscan_evaluation.csv", "a") as file:
        file.write("epsilon, minimum points, n_cluster, intra-clusters distance, inter-clusters mean distance\n")
    
    for index, (dataset, p2p_distance_function, minimum_points, epsilon) in enumerate(possible_combinations, start=1):
        print("-"* 100)
        print(f"combination {index}:")

        algorithm = DBSCAN(
            minimum_points=minimum_points, 
            epsilon=epsilon, 
            p2p_distance_function=p2p_distance_functions[p2p_distance_function]
        )

        start = time()
        clusters, outliers = algorithm(dataset=dataset)
        finish = time()

        # if len(clusters) in (0, 1):
        #     continue
        
        print(f"\tminimum points = {minimum_points}")
        print(f"\tepsilon = {epsilon}")
        print(f"\tp2p distance function = {p2p_distance_function}\n")

        print("*" * 100)
        print(f"done clustering in {round(finish - start)} seconds")

        print(f"there are {len(clusters)} clusters")
        print(f"there are {len(outliers)} outliers")

        measure_1 = n_clusters(clusters=clusters)
        measure_2 = intraclusters_distance(clusters=clusters, p2p_distance_function=p2p_distance_functions[p2p_distance_function])
        measure_3 = interclusters_distance(clusters=clusters, c2c_distance_function=minimal_distance(p2p_distance_functions[p2p_distance_function]))

        print("*" * 100)
        print(f"measure 1 (number of clusters): {measure_1}")
        print(f"measure 2 (intra-clusters distance): {measure_2}")
        print(f"measure 3 (inter-clusters mean distance): {measure_3}")

        with open("dbscan_evaluation.csv", "a") as file:
            file.write(f"{epsilon}, {minimum_points}, {measure_1}, {measure_2}, {measure_3}\n")

        print("*" * 100)
        # quit = input("want to quit? [y/(N)]: ")

        # if quit.lower() == "y":
        #     break