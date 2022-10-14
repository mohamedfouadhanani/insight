from flask import Blueprint, redirect, render_template, request
from matplotlib import pyplot as plt
import pandas as pd

from dm.analysis import find_mean, find_median, find_modes, quartiles, find_outliers, summetry

import settings

analysis_blueprint = Blueprint("analysis", __name__)


@analysis_blueprint.route("/<string:attribute>", methods=["GET"])
def index_analysis(attribute):
    if settings.dataset is None:
        return redirect("/load/")

    if attribute not in settings.dataset.columns:
        return redirect("/dataset/")

    # compute mean, median, modes
    modes = find_modes(settings.dataset[attribute])

    info = {
        "mean": "N/A",
        "median": "N/A",
        "q0": "N/A", "q1": "N/A", "q2": "N/A", "q3": "N/A", "q4": "N/A",
        "symmetry": "N/A",
        "iqr": "N/A",
        "modes": ", ".join([str(mode) for mode in modes])
    }
    outliers = pd.DataFrame()

    show_boxplot = False
    show_histogram = False

    if settings.dataset[attribute].dtype != "object":
        mean = find_mean(settings.dataset[attribute])
        _, median = find_median(settings.dataset[attribute])

        # compute quartiles (q0 -> q4) & IQR
        q0, q1, q2, q3, q4 = quartiles(settings.dataset[attribute])
        iqr = q3 - q1

        # compute symmetry
        symmetry_dictionary = {0: "symmetric", 1: "skewed to the right", -1: "skewed to the left"}
        attribute_symmetry_value = summetry(settings.dataset[attribute])
        attribute_symmetry = symmetry_dictionary[attribute_symmetry_value]

        # find outliers
        outliers_indicies = find_outliers(settings.dataset[attribute])
        outliers = settings.dataset.iloc[outliers_indicies]

        # draw & save boxplot
        plt.boxplot(settings.dataset[attribute])
        plt.savefig("static/images/boxplot.png")
        plt.close()

        info = {
            "mean": mean,
            "median": median,
            "q0": q0, "q1": q1, "q2": q2, "q3": q3, "q4": q4,
            "symmetry": attribute_symmetry,
            "iqr": iqr,
            "modes": ", ".join([str(mode) for mode in modes])
        }

        show_boxplot = True
    else:
        show_histogram = True
        plt.hist(settings.dataset[attribute])
        plt.savefig("static/images/histogram.png")
        plt.close()

    return render_template(
        "/analysis/index.html", title=f"Attribute Analysis | {attribute}", attribute=attribute, info=info,
        outliers=outliers, columns=settings.dataset.columns, show_boxplot=show_boxplot, show_histogram=show_histogram)


@analysis_blueprint.route("/<string:attribute_1>/scatterplot", methods=["POST"])
def scatter_plot_analysis(attribute_1):
    attribute_2 = request.form["attribute"]

    X = settings.dataset[attribute_1]
    Y = settings.dataset[attribute_2]

    # if attribute_1 is categorical then encode
    if settings.dataset[attribute_1].dtype == "object":
        attribute_1_unique_values = set(settings.dataset[attribute_1])
        attribute_1_unique_values_dictionary = {value: index for index, value in enumerate(attribute_1_unique_values)}
        X = [attribute_1_unique_values_dictionary[value] for value in settings.dataset[attribute_1]]

    # if attribute_2 is categorical then encode
    if settings.dataset[attribute_2].dtype == "object":
        attribute_2_unique_values = set(settings.dataset[attribute_2])
        attribute_2_unique_values_dictionary = {value: index for index, value in enumerate(attribute_2_unique_values)}
        Y = [attribute_2_unique_values_dictionary[value] for value in settings.dataset[attribute_2]]

    plt.scatter(X, Y)
    plt.xlabel(attribute_1)
    plt.ylabel(attribute_2)
    plt.savefig("static/images/scatterplot.png")
    plt.close()

    return render_template("analysis/scatterplot.html",
                           title=f"Attribute Analysis | Scatter Plot {attribute_1} of and {attribute_2}",
                           attribute_1=attribute_1, attribute_2=attribute_2)


@analysis_blueprint.route("/<string:attribute>/histogram", methods=["POST"])
def histogram_analysis(attribute):
    n_bins = int(request.form["nbins"])
    plt.hist(settings.dataset[attribute], bins=n_bins)
    plt.savefig("static/images/histogram.png")
    plt.close()

    return render_template("analysis/histogram.html",
                           title=f"Attribute Analysis | Histogram of attribute {attribute}", attribute=attribute)
