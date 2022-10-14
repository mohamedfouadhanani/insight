from flask import Blueprint, redirect, render_template, request

import settings

dataset_blueprint = Blueprint("dataset", __name__)


@dataset_blueprint.route("/", methods=["GET"])
def index_dataset():
    if settings.dataset is None:
        return redirect("/load/")

    m, n = settings.dataset.shape

    dtypes = settings.dataset.dtypes.to_dict()
    dtypes = {key: value if value != "object" else "string" for key, value in dtypes.items()}

    return render_template(
        "dataset.html", title="Visualizing the dataset", samples=m, attributes=n, dtypes=dtypes,
        dataset=settings.dataset, columns=settings.dataset.columns)


@dataset_blueprint.route("/delete/<int:row_idx>", methods=["GET"])
def delete_row(row_idx):
    settings.dataset = settings.dataset.drop([row_idx])

    return redirect(request.referrer)
