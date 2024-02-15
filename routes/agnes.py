from flask import Blueprint, render_template, request, redirect
import pandas as pd

from dm.agnes.agnes import Agnes
from dm.agnes.distances import difference, minimal_distance, maximal_distance, mean_distance

import settings

# EXTRA CODE
from agnes import random_points

agnes_blueprint = Blueprint("agnes", __name__)

@agnes_blueprint.route("/", methods=["GET"])
def get_agnes_params():
    if settings.dataset is None:
        return redirect("/load/")

    # minimum points, epsilon
    params = {
        "agglomerative_function": {
            "name": "agglomerative function",
            "values": {
                "minimal_distance": "minimal distance",
                "maximal_distance": "maximal distance",
                "mean_distance": "mean distance",
            }
        }
    }

    return render_template("agnes/index.html", title="AGNES Clustering", params=params)


@agnes_blueprint.route("/", methods=["POST"])
def post_agnes_params():
    if settings.dataset is None:
        return redirect("/load/")

    agglomerative_functions = {
        "minimal_distance": minimal_distance,
        "maximal_distance": maximal_distance,
        "mean_distance": mean_distance,
    }
    
    # get parameters
    # transform to appropriate datatype
    agglomerative_function = request.form["agglomerative_function"]

    # create an instance of agnes
    algorithm = Agnes(c2c_distance_function=agglomerative_functions[agglomerative_function](difference))

    # transform the dataset to list of tuples
    df = pd.read_excel("Dataset1_pretraitement_complet.xlsx")
    dataset = list(df.itertuples(index=False, name=None))

    mini_dataset = random_points(dataset, 10)

    # run the instance
    history = algorithm(dataset=mini_dataset)

    # columns
    columns = df.columns

    # return results
    return render_template("agnes/results.html", title="AGNES Clustering | Results", history=history, columns=columns)