from flask import Blueprint, redirect, render_template, request
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


from dm.analysis import attribute_type, chi2, encode, find_mean, find_median, find_modes, quartiles, find_outliers, symmetry, pearson_correlation

import settings

analysis_blueprint = Blueprint("analysis", __name__)


@analysis_blueprint.route("/<string:attribute>", methods=["GET"])
def index_analysis(attribute):
    if settings.dataset is None:
        return redirect("/load/")

    if attribute not in settings.dataset.columns:
        return redirect("/dataset/")

    # find missing values
    missing_indicies = settings.dataset.index[settings.dataset[attribute].isnull()].tolist()
    missings = settings.dataset.iloc[missing_indicies]

    # compute mean, median, modes
    modes = find_modes(settings.dataset[settings.dataset[attribute].notna()][attribute])

    info = {
        "mean": "N/A",
        "median": "N/A",
        "q0": "N/A", "q1": "N/A", "q2": "N/A", "q3": "N/A", "q4": "N/A",
        "symmetry": "N/A",
        "iqr": "N/A",
        "unique": settings.dataset[attribute].nunique(),
        "type": " ".join(attribute_type(settings.dataset, attribute)),
        "modes": ", ".join([str(mode) for mode in modes])
    }
    outliers = pd.DataFrame()

    show_boxplot = False
    show_histogram = False
    show_normalization = False
    show_discretization = False

    # discretization methods
    discretization_methods = ["equal-frequency", "equal-width"]

    attribute_types = attribute_type(dataset=settings.dataset, attribute=attribute)

    if set(["discret", "nominal"]).issubset(attribute_types):
        replacement_methods = ["unknown", "mode"]

    if set(["discret", "ordinal"]).issubset(attribute_types):
        replacement_methods = ["mode"]

    if set(["continue"]).issubset(attribute_types):
        # discretization
        show_discretization = True

        replacement_methods = ["mean", "median", "mode", "minimum"]

        show_normalization = True

        mean = find_mean(settings.dataset[settings.dataset[attribute].notna()][attribute])
        _, median = find_median(settings.dataset[settings.dataset[attribute].notna()][attribute])

        # compute quartiles (q0 -> q4) & IQR
        q0, q1, q2, q3, q4 = quartiles(settings.dataset[settings.dataset[attribute].notna()][attribute])
        iqr = q3 - q1

        # compute symmetry
        symmetry_dictionary = {0: "symmetric", 1: "asymmetric positive", -1: "asymmetric negative", -2: "non-symmetric"}
        attribute_symmetry_value = symmetry(settings.dataset[settings.dataset[attribute].notna()][attribute])
        attribute_symmetry = symmetry_dictionary[attribute_symmetry_value]

        # find outliers
        outliers_indicies = find_outliers(settings.dataset[settings.dataset[attribute].notna()][attribute])
        outliers = settings.dataset.iloc[outliers_indicies]

        # draw & save boxplot
        plt.boxplot(settings.dataset[settings.dataset[attribute].notna()][attribute])
        plt.title(f"boxplot of attribute {attribute}")
        plt.savefig("static/images/boxplot.png")
        plt.close()

        info = {
            "mean": round(mean, settings.round_to),
            "median": round(median, settings.round_to),
            "q0": round(q0, settings.round_to),
            "q1": round(q1, settings.round_to),
            "q2": round(q2, settings.round_to),
            "q3": round(q3, settings.round_to),
            "q4": round(q4, settings.round_to),
            "symmetry": attribute_symmetry, "iqr": round(iqr, settings.round_to),
            "unique": settings.dataset[attribute].nunique(),
            "type": " ".join(attribute_type(settings.dataset, attribute)),
            "modes": ", ".join([str(round(mode, settings.round_to)) for mode in modes])}

        show_boxplot = True
    else:
        show_histogram = True

        plt.hist(settings.dataset[settings.dataset[attribute].notna()][attribute])
        plt.title(f"histogram of attribute {attribute}")
        plt.savefig("static/images/histogram.png")
        plt.close()

    return render_template(
        "/analysis/index.html", title=f"Attribute Analysis | {attribute}", attribute=attribute, info=info,
        outliers=outliers, columns=settings.dataset.columns, show_boxplot=show_boxplot, show_histogram=show_histogram,
        show_normalization=show_normalization, missings=missings, replacement_methods=replacement_methods,
        show_discretization=show_discretization, discretization_methods=discretization_methods)


@ analysis_blueprint.route("/<string:attribute_1>/scatterplot", methods=["POST"])
def scatter_plot_analysis(attribute_1):
    attribute_2 = request.form["attribute"]

    correlation_coefficient = 0
    show_correlation_coefficient = False

    X = settings.dataset[settings.dataset[attribute_1].notna() & settings.dataset[attribute_2].notna()][attribute_1]
    Y = settings.dataset[settings.dataset[attribute_1].notna() & settings.dataset[attribute_2].notna()][attribute_2]

    # if attribute_1 is categorical then encode
    if "nominal" in attribute_type(settings.dataset, attribute_1):
        X = encode(X)

    # if attribute_2 is categorical then encode
    if "nominal" in attribute_type(settings.dataset, attribute_2):
        Y = encode(Y)

    plt.scatter(X, Y)
    plt.xlabel(attribute_1)
    plt.ylabel(attribute_2)
    plt.title(f"scatter plot of attributes {attribute_1} and {attribute_2}")
    plt.savefig("static/images/scatterplot.png")
    plt.close()

    if "continue" in attribute_type(
            settings.dataset, attribute_1) and "continue" in attribute_type(
            settings.dataset, attribute_2):
        correlation_coefficient = round(pearson_correlation(X, Y), 2)
        show_correlation_coefficient = True

    if "discret" in attribute_type(
            settings.dataset, attribute_1) and "discret" in attribute_type(
            settings.dataset, attribute_2):

        if "ordinal" in attribute_type(settings.dataset, attribute_1):
            # transform to a python list
            X = encode(X)

        if "ordinal" in attribute_type(settings.dataset, attribute_2):
            # transform to a python list
            X = encode(Y)

        correlation_coefficient = round(chi2(X, Y), 2)
        show_correlation_coefficient = True

    return render_template("analysis/scatterplot.html",
                           title=f"Attribute Analysis | Scatter Plot {attribute_1} of and {attribute_2}",
                           attribute_1=attribute_1, attribute_2=attribute_2,
                           correlation_coefficient=correlation_coefficient,
                           show_correlation_coefficient=show_correlation_coefficient)


@ analysis_blueprint.route("/<string:attribute>/histogram", methods=["POST"])
def histogram_analysis(attribute):
    n_bins = int(request.form["nbins"])
    plt.hist(settings.dataset[settings.dataset[attribute].notna()][attribute], bins=n_bins)
    plt.ylabel("Frequency")
    plt.title(f"histogram of attribute {attribute}")
    plt.savefig("static/images/histogram.png")
    plt.close()

    return render_template("analysis/histogram.html",
                           title=f"Attribute Analysis | Histogram of attribute {attribute}", attribute=attribute)
