from flask import Blueprint, redirect, render_template, request
from dm.apriori import apriori

import settings

prediction_blueprint = Blueprint("prediction", __name__)

@prediction_blueprint.route("/", methods=["GET"])
def index_get():
    prediction_algorithms = {
        "decision_tree": "decision tree",
        "random_forest": "random forest",
    }

    dtypes = settings.dataset.dtypes
    
    return render_template("prediction/index.html", title="Prediction", prediction_algorithms=prediction_algorithms, dtypes=dtypes)

@prediction_blueprint.route("/", methods=["POST"])
def index_post():
    prediction_algorithm = request.form["prediction_algorithm"]
    dtypes = settings.dataset.dtypes

    form_configuration = {"prediction_algorithm": prediction_algorithm}
    for column, dtype in dtypes.items():
        if dtype != "object":
            column = column.strip()
            form_configuration.update({column: float(request.form[column])})
        else:
            column = column.strip()
            form_configuration.update({column: request.form[column]})
    
    print(form_configuration)

    return ""