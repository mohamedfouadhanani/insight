import os

os.environ["PYTHONDONTWRITEBYTECODE"] = "abc"

from flask import Flask, redirect, make_response, request
from routes.load import loading_blueprint
from routes.dataset import dataset_blueprint
from routes.analysis import analysis_blueprint
from routes.pretreatment import pretreatment_blueprint
from routes.apriori import apriori_blueprint
from routes.prediction import prediction_blueprint
from routes.dbscan import dbscan_blueprint
from routes.agnes import agnes_blueprint

import settings

# settings.init_dev()
settings.init()

app = Flask(__name__)

app.register_blueprint(loading_blueprint, url_prefix="/load")
app.register_blueprint(dataset_blueprint, url_prefix="/dataset")
app.register_blueprint(analysis_blueprint, url_prefix="/analysis")
app.register_blueprint(pretreatment_blueprint, url_prefix="/pretreatment")
app.register_blueprint(apriori_blueprint, url_prefix="/apriori")
app.register_blueprint(prediction_blueprint, url_prefix="/prediction")
app.register_blueprint(dbscan_blueprint, url_prefix="/dbscan")
app.register_blueprint(agnes_blueprint, url_prefix="/agnes")


@app.route("/", methods=["GET"])
def index():
    return redirect("/load")


@app.route("/drop", methods=["GET"])
def drop():
    settings.dataset = None
    return redirect("/load")


@app.route("/save", methods=["GET"])
def save():
    response = make_response(settings.dataset.to_csv())
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


@app.route("/reset", methods=["GET"])
def reset():
    settings.init()

    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True)
