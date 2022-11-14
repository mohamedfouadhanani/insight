import pandas as pd
from itertools import combinations, product

with open("dataset2.xlsx", "rb") as file:
    file_content = file.read()

dataset = pd.read_excel(file_content)

round_to = 2

transactions = {
    "T1": set([1, 2, 5]),
    "T2": set([2, 4]),
    "T3": set([2, 3]),
    "T4": set([1, 2, 4]),
    "T5": set([1, 3]),
    "T6": set([2, 3]),
    "T7": set([1, 3]),
    "T8": set([1, 2, 3, 5]),
    "T9": set([1, 2, 3]),
}

def candidate_sets(transactions, minimum_support):
    candidates = {}
    k = 1

    items = set([item for transaction in transactions for item in transactions[transaction]])
    
    while True:
        candidate_i = tuple()
        
        for combination in combinations(items, k):   
            count = 0
            for _, itemset in transactions.items():
                if itemset.issuperset(combination):
                    count += 1
            
            if count >= minimum_support:
                candidate_i += (combination, )

        if not candidate_i:
            break

        candidates[k] = candidate_i
        k += 1
    
    return candidates

def association_rules(candidates):
    rules = []

    try:
        for combination in candidates[2]:
            item_1, item_2 = combination

            item_1 = set([item_1])
            item_2 = set([item_2])

            rules.append((item_1, item_2))
            rules.append((item_2, item_1))

        candidates = {k: itemset for k, itemset in candidates.items() if k not in [1, 2]}

        for k, candidate_combinations in candidates.items():
            for combination in candidate_combinations:
                for i in range(1, k):
                    combination = set(combination)
                    for subcombination in combinations(combination, i):
                        premise = set(subcombination)
                        consequence = combination.difference(premise)
                        rules.append((premise, consequence))
    except:
        pass
    
    return rules

def support(transactions, item):
    n_transactions = len(transactions)

    if n_transactions == 0:
        raise ValueError("Empty Transactions Table...")
        
    count = 0

    for _, transaction_items in transactions.items():
        if transaction_items.issuperset(item):
            count += 1
    
    result = count / n_transactions
    
    return result

def confidence(transactions, item_1, item_2):
    term_1 = support(transactions=transactions, item=item_1.union(item_2))
    term_2 = support(transactions=transactions, item=item_1)

    result = round(term_1 / term_2, round_to)

    return result

def lift(transactions, item_1, item_2):
    term_1 = support(transactions=transactions, item=item_1.union(item_2))
    term_2 = support(transactions=transactions, item=item_1)
    term_3 = support(transactions=transactions, item=item_2)

    term_4 = term_2 * term_3

    result = round(term_1 / term_4, round_to)

    return result

def apriori(transactions, minimum_support, minimum_confidence):
    candidates = candidate_sets(transactions=transactions, minimum_support=minimum_support)

    rules = association_rules(candidates=candidates)

    # removing rules with confidence lower then minimum confidence
    rules = [(premise, consequence) for premise, consequence in rules if confidence(transactions, item_1=premise, item_2=consequence) >= minimum_confidence]

    # sorting rules by lift
    rules = sorted(rules, key=lambda rule: lift(transactions=transactions, item_1=rule[0], item_2=rule[1]), reverse=True)

    return rules, candidates

minimum_support = 3
minimum_confidence = 0.8

def main(dataset):
    dataset["id"] = dataset["videoCategoryId"]
    dataset["items"] = dataset["id"].astype(str) + ", " + dataset["definition"]

    dataset = dataset.drop("videoCategoryLabel", axis=1)
    dataset = dataset.drop("videoCategoryId", axis=1)
    dataset = dataset.drop("definition", axis=1)
    dataset = dataset.drop("id", axis=1)

    transactions = {watcher: set() for watcher in dataset["Watcher"].unique()}
    for value in dataset.values.tolist():
        watcher = value[0]
        item = value[1]
        transactions[watcher].add(item)

    
    # minimum_support, minimum_confidence, number_of_rules, minimum_lift, maximum_lift
    n = len(transactions)
    minimum_support_values = [10, 20, 30, 50, 60, 80]
    minimum_support_values = [int(value * n * 0.01) for value in minimum_support_values]

    minimum_confidence_values = [10, 20, 30, 50, 70]
    minimum_confidence_values = [round(value * 0.01, round_to) for value in minimum_confidence_values]

    with open("results.csv", "w") as file:
        file.write("minimum_support, minimum_confidence, number_of_rules, minimum_lift, maximum_lift\n")
        for minimum_support, minimum_confidence in product(minimum_support_values, minimum_confidence_values):
            rules = apriori(transactions=transactions, minimum_support=minimum_support, minimum_confidence=minimum_confidence)
            number_of_rules = len(rules)
            minimum_lift = 0
            maximum_lift = 0
            if number_of_rules != 0:
                premise, consequence = rules[-1]
                minimum_lift = lift(transactions=transactions, item_1=premise, item_2=consequence)
                premise, consequence = rules[0]
                maximum_lift = lift(transactions=transactions, item_1=premise, item_2=consequence)
            file.write(f"{minimum_support}, {minimum_confidence}, {number_of_rules}, {minimum_lift}, {maximum_lift}\n")

    
    

if __name__ == "__main__":
    main(dataset)