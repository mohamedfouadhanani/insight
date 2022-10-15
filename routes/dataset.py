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
        "dataset/index.html", title="Visualizing the dataset", samples=m, attributes=n, dtypes=dtypes,
        dataset=settings.dataset, columns=settings.dataset.columns)


@dataset_blueprint.route("/delete/<int:row_idx>", methods=["GET"])
def delete_row(row_idx):
    if settings.dataset is None:
        return redirect("/load/")

    settings.dataset = settings.dataset.drop([row_idx])

    return redirect(request.referrer)


@dataset_blueprint.route("/edit/<int:row_idx>", methods=["GET"])
def get_edit_row(row_idx):
    if settings.dataset is None:
        return redirect("/load/")

    sample = settings.dataset.iloc[row_idx]
    dtypes = settings.dataset.dtypes.to_dict()

    for key, item in dtypes.items():
        print(key, item, sample[key])

    return render_template("dataset/edit.html", title="Editing a sample", sample=sample, dtypes=dtypes, row_idx=row_idx)


@dataset_blueprint.route("/edit/<int:row_idx>", methods=["POST"])
def post_edit_row(row_idx):
    if settings.dataset is None:
        return redirect("/load/")

    for column in settings.dataset.columns:
        dtype = settings.dataset[column].dtype

        value = request.form[column]
        settings.dataset.at[row_idx, column] = value

        if dtype != "object":
            settings.dataset[column] = settings.dataset[column].astype(dtype)

    return redirect("/dataset/")
