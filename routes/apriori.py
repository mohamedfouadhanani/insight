from flask import Blueprint, redirect, render_template, request
from dm.apriori import apriori

import settings

apriori_blueprint = Blueprint("apriori", __name__)

@apriori_blueprint.route("/", methods=["GET"])
def index_get():
    extraction_algorithm = ["apriori", "fp-growth", "eclat"]
    return render_template("apriori/index.html", title="Association Rules", extraction_algorithm=extraction_algorithm)

@apriori_blueprint.route("/", methods=["POST"])
def index_post():
    extraction_algorithm = request.form["extraction_algorithm"]
    minimum_support = int(request.form["minimum_support"])
    minimum_confidence = int(request.form["minimum_confidence"])

    settings.dataset["id"] = settings.dataset["videoCategoryId"]
    settings.dataset["items"] = settings.dataset["id"].astype(str) + ", " + settings.dataset["definition"]

    transactions = {watcher: set() for watcher in settings.dataset["Watcher"].unique()}
    
    for _, row in settings.dataset.iterrows():
        watcher = row["Watcher"]
        item = row["items"]
        transactions[watcher].add(item)
    
    n = len(transactions)
    minimum_support = int(minimum_support * n * 0.01)
    minimum_confidence = round(minimum_confidence * 0.01, settings.round_to)
    
    rules, candidates = apriori(transactions=transactions, minimum_support=minimum_support, minimum_confidence=minimum_confidence)
    print(candidates)

    new_rules = []
    for premise, consequence in rules:
        new_premise = " AND ".join([item for item in premise])
        new_consequence = " AND ".join([item for item in consequence])

        new_rules.append((new_premise, new_consequence))
    

    settings.dataset = settings.dataset.drop("id", axis=1)
    settings.dataset = settings.dataset.drop("items", axis=1)

    return render_template("apriori/rules.html", title="Association Rules", rules=new_rules, candidates=candidates)


@apriori_blueprint.route("/recommend", methods=["POST"])
def recommend_post():
    items = request.form["items"]
    items = items.split(";")
    items = [item.strip() for item in items if len(item) > 0]

    itemset = set(items)

    minimum_support = int(request.form["minimum_support"])
    minimum_confidence = int(request.form["minimum_confidence"])

    settings.dataset["id"] = settings.dataset["videoCategoryId"]
    settings.dataset["items"] = settings.dataset["id"].astype(str) + ", " + settings.dataset["definition"]

    transactions = {watcher: set() for watcher in settings.dataset["Watcher"].unique()}
    
    for _, row in settings.dataset.iterrows():
        watcher = row["Watcher"]
        item = row["items"]
        transactions[watcher].add(item)
    
    n = len(transactions)
    minimum_support = int(minimum_support * n * 0.01)
    minimum_confidence = round(minimum_confidence * 0.01, settings.round_to)
    
    rules, _ = apriori(transactions=transactions, minimum_support=minimum_support, minimum_confidence=minimum_confidence)
    
    recommendations = [tuple(item.split(", ")) for premise, consequence in rules for item in consequence if itemset.issuperset(premise)]

    settings.dataset = settings.dataset.drop("id", axis=1)
    settings.dataset = settings.dataset.drop("items", axis=1)

    return render_template("apriori/recommendation.html", title="Recommendations", recommendations=recommendations)