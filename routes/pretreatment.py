from flask import Blueprint, redirect, render_template, request
from dm.analysis import attribute_type, find_outliers
from dm.pretreatment import fill_mean, fill_median, fill_mode, fill_unknown, min_max_normalization, z_score_normalization
import settings

pretreatment_blueprint = Blueprint("pretreatment", __name__)


@pretreatment_blueprint.route("/<string:attribute>/delete", methods=["GET"])
def delete_attribute(attribute):
    if settings.dataset is None:
        return redirect("/load/")

    if attribute not in settings.dataset.columns:
        return redirect("/dataset/")

    settings.dataset.drop(attribute, axis=1, inplace=True)

    return redirect("/dataset/")


@pretreatment_blueprint.route("/<string:attribute>/outliers/delete", methods=["GET"])
def delete_outliers(attribute):
    if settings.dataset is None:
        return redirect("/load/")

    if attribute not in settings.dataset.columns:
        return redirect("/dataset/")

    if "continue" in attribute_type(settings.dataset, attribute):
        outliers_indicies = find_outliers(settings.dataset[attribute])
        settings.dataset.drop(outliers_indicies, inplace=True)

    return redirect(f"/analysis/{attribute}")


@pretreatment_blueprint.route("/<string:attribute>/normalization", methods=["POST"])
def normalize(attribute):
    normalization_method = request.form["normalization"]

    if normalization_method == "minmax":
        # acquire minimum & maximum
        minimum = float(request.form["minimum"])
        maximum = float(request.form["maximum"])

        # minmax normalization
        settings.dataset[attribute] = min_max_normalization(
            settings.dataset[attribute], minimum=minimum, maximum=maximum)

        return redirect(request.referrer)

    # apply zscore normalization
    settings.dataset[attribute] = z_score_normalization(settings.dataset[attribute])

    return redirect(request.referrer)


@pretreatment_blueprint.route("/duplicates/delete", methods=["GET"])
def delete_duplicates():
    settings.dataset.drop_duplicates(inplace=True)
    return redirect(request.referrer)


@pretreatment_blueprint.route("/<string:attribute>/missing", methods=["POST"])
def replace_missing_values(attribute):
    if settings.dataset is None:
        return redirect("/load/")

    if attribute not in settings.dataset.columns:
        return redirect("/dataset/")

    method = request.form["missing_values_replacement"]

    method_functions = {
        "mean": fill_mean,
        "median": fill_median,
        "mode": fill_mode,
        "unknown": fill_unknown,
    }

    try:
        method_functions[method](settings.dataset, attribute)
    except:
        pass

    return redirect(request.referrer)
