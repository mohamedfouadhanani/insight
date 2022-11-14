from flask import Blueprint, render_template, request, redirect
import os
from io import StringIO
import pandas as pd

import settings

loading_blueprint = Blueprint("load", __name__)


@loading_blueprint.route("/", methods=["GET"])
def get_load():
    if settings.dataset is not None:
        return redirect("/dataset")
    return render_template("load.html", title="Loading a dataset")


@loading_blueprint.route("/", methods=["POST"])
def post_load():
    if settings.dataset is not None:
        return redirect("/dataset")
    # update the dataset global variable so it prevents the redirect
    file = request.files['file']
    file_content = file.read()

    _, file_extension = os.path.splitext(file.filename)

    if file_extension == ".xlsx":
        data = pd.read_excel(file_content)
    else:
        data_string = file_content.decode("ascii")
        data = pd.read_csv(StringIO(data_string))

    data = data.rename(columns=lambda x: x.strip())
    settings.dataset = data
    # set dataset variable
    return redirect("/dataset/")
