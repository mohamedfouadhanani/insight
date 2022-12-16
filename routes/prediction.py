from flask import Blueprint, render_template, request
import pandas as pd
import numpy as np

import re

import settings

prediction_blueprint = Blueprint("prediction", __name__)

@prediction_blueprint.route("/", methods=["GET"])
def index_get():
    prediction_algorithms = {
        "decision_tree": "decision tree",
        "decision_tree_with_id3": "decision tree with id3",
        "random_forest": "random forest",
    }

    dtypes = settings.dataset.dtypes
    dtypes = {name: dtype for name, dtype in dtypes.items() if name not in ["Attrition", "EmployeeCount", "EmployeeNumber", "Over18", "PerformanceRating", "StandardHours"]}
    
    with open("Dataset1_pretraitement_complet.xlsx", "rb") as file:
        file_content = file.read()
    
    # get the class
    df = pd.read_excel(file_content)
    sample = df.iloc[20]
    
    return render_template("prediction/index.html", title="Prediction", prediction_algorithms=prediction_algorithms, dtypes=dtypes, sample=sample)

@prediction_blueprint.route("/", methods=["POST"])
def index_post():
    prediction_algorithms = {
        "decision_tree": settings.decision_tree_model,
        "random_forest": settings.random_forest_model,
        "decision_tree_with_id3": settings.decision_tree_with_id3_model
    }

    chosen_prediction_algorithm = request.form["prediction_algorithm"]
    prediction_algorithm = prediction_algorithms[chosen_prediction_algorithm]
    
    dtypes = settings.dataset.dtypes
    dtypes = {name: dtype for name, dtype in dtypes.items() if name not in ["Attrition", "EmployeeCount", "EmployeeNumber", "Over18", "PerformanceRating", "StandardHours"]}

    pattern = re.compile("[0-9]+(.[0-9])*")

    form_sample = []
    for column, dtype in dtypes.items():
        value = request.form[column].strip()
        boolean_value = bool(pattern.match(value))

        if boolean_value:
            form_sample.append(float(value))
        else:
            form_sample.append(value)
    
    print(form_sample)
    form_sample = np.array(form_sample, dtype="O")
    print(form_sample)
    
    sample_prediction = prediction_algorithm.predict(np.array([form_sample], dtype="O"))
    # print(f"prediction is {sample_prediction}")
    # print(type(sample_prediction))

    sample_prediction = int(sample_prediction[0])
    # print(f"prediction is {sample_prediction}")
    # print(type(sample_prediction))

    sample_prediction = sample_prediction == 1
    # print(f"prediction is {sample_prediction}")
    # print(type(sample_prediction))

    return render_template("prediction/result.html", title="Prediction", prediction=sample_prediction)


@prediction_blueprint.route("/tests/<int:row>", methods=["GET"])
def tests_get(row):
    prediction_algorithms = {
        "decision_tree": "decision tree",
        "decision_tree_with_id3": "decision tree with id3",
        "random_forest": "random forest",
    }

    dtypes = settings.dataset.dtypes
    dtypes = {name: dtype for name, dtype in dtypes.items() if name not in ["Attrition", "EmployeeCount", "EmployeeNumber", "Over18", "PerformanceRating", "StandardHours"]}
    
    with open("Dataset1_pretraitement_complet.xlsx", "rb") as file:
        file_content = file.read()
    
    # get the class
    df = pd.read_excel(file_content)
    sample = df.iloc[row]
    
    return render_template("prediction/index.html", title="Prediction", prediction_algorithms=prediction_algorithms, dtypes=dtypes, sample=sample)