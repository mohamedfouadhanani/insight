from flask import Blueprint, render_template, request, redirect
import pandas as pd

from dm.dbscan.dbscan import DBSCAN
from dm.dbscan.distances import similarity

import settings

dbscan_blueprint = Blueprint("dbscan", __name__)


@dbscan_blueprint.route("/", methods=["GET"])
def get_dbscan_params():
    if settings.dataset is None:
        return redirect("/load/")

    # minimum points, epsilon
    params = {
        "minimum_points": {
            "name": "minimum points",
            "value": 1
        },
        "epsilon": {
            "name": "epsilon",
            "value": 2
        }
    }

    return render_template("dbscan/index.html", title="DBSCAN Clustering", params=params)


@dbscan_blueprint.route("/", methods=["POST"])
def post_dbscan_params():
    if settings.dataset is None:
        return redirect("/load/")
    
    # get parameters
    # transform to appropriate datatype
    minimum_points = int(request.form["minimum_points"])
    epsilon = float(request.form["epsilon"])

    # create an instance of DBSCAN
    algorithm = DBSCAN(minimum_points=minimum_points, epsilon=epsilon, p2p_distance_function=similarity)

    # transform the dataset to list of tuples
    df = pd.read_excel("Dataset1_pretraitement_complet.xlsx")
    dataset = list(df.itertuples(index=False, name=None))

    # run the instance
    clusters, outliers = algorithm(dataset)
    for cluster in clusters:
        cluster.points = cluster.points[:min(10, len(cluster.points))]

    # columns
    columns = df.columns

    # return results
    return render_template("dbscan/results.html", title="DBSCAN Clustering | Results", clusters=clusters, outliers=outliers, columns=columns)