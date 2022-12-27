import dill
from sklearn.metrics import confusion_matrix, f1_score, classification_report, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import os

from time import time

from dm import DT_with_ID3
from dm import Decision_tree
from dm import Random_forest

def get_metrics(y_test, y_pred):
    print("confusion_matrix(y_test, y_pred).ravel()")
    print(confusion_matrix(y_test, y_pred).ravel())
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    specificity = tn / (tn+fp)
    # specificity = None

    score = f1_score(y_test, y_pred)

    metrics = {"f1_score": score, "specificity": specificity}
    return metrics

def load_models():
    decision_tree_with_id3_model = None
    with open("decision_tree_with_id3.model", "rb") as dill_file:
        decision_tree_with_id3_model = dill.load(dill_file)
    print("done getting decision tree with ID3 model...")

    decision_tree_model = None
    with open("decision_tree.model", "rb") as dill_file:
        decision_tree_model = dill.load(dill_file)
    print("done getting decision tree model...")

    random_forest_model = None
    with open("random_forest.model", "rb") as dill_file:
        random_forest_model = dill.load(dill_file)
    print("done getting random forest model...")

    return decision_tree_with_id3_model, decision_tree_model, random_forest_model

def load_split_dataset():
    with open("Dataset1_pretraitement_complet.xlsx", "rb") as file:
        file_content = file.read()
    
    df = pd.read_excel(file_content)
    
    # get class attribut
    y = df["Attrition"].to_numpy()
    # print("shape of Y : ", y.shape)

    df = df.drop("Attrition", axis=1)
    df = df.drop("Unnamed: 0", axis=1)

    # X with 29 features
    X = df.to_numpy()
    # print("shape of X : ", X.shape)

    # split the dataset into training set (80%) and testing set (20%)  
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    

    return X_train, y_train, X_test, y_test

def get_sub_predictions(y_test, y_pred):
    # where y_test is 0
    where_y_test_0 = [index for index, g_truth in enumerate(y_test) if g_truth == 0]
    y_pred_0 = [y_pred[index] for index in where_y_test_0]
    y_test_0 = [0] * len(y_pred_0)

    # where y_test is 1
    where_y_test_1 = [index for index, g_truth in enumerate(y_test) if g_truth == 1]
    y_pred_1 = [y_pred[index] for index in where_y_test_1]
    y_test_1 = [1] * len(y_pred_1)

    return y_pred_0, y_test_0, y_pred_1, y_test_1

def main():
    # model loading
    decision_tree_with_id3_model, decision_tree_model, random_forest_model = load_models()

    # dataset loading
    X_train, y_train, X_test, y_test = load_split_dataset()

    # prediction
    # y_pred_decision_tree_with_id3_model = decision_tree_with_id3_model.predict(X_test)
    # y_pred_decision_tree_model = decision_tree_model.predict(X_test)
    # y_pred_random_forest_model = random_forest_model.predict(X_test)

    # evaluation
    # id3_metrics = get_metrics(y_test, y_pred_decision_tree_with_id3_model)
    # dt_metrics = get_metrics(y_test, y_pred_decision_tree_model)
    # rf_metrics = get_metrics(y_test, y_pred_random_forest_model)

    # print("global")
    # print(f"global specificity of id3: {id3_metrics['specificity']}")
    # print(f"global specificity of dt: {dt_metrics['specificity']}")
    # print(f"global specificity of rf: {rf_metrics['specificity']}")

    # print(f"global f1_score of id3: {id3_metrics['f1_score']}")
    # print(f"global f1_score of dt: {dt_metrics['f1_score']}")
    # print(f"global f1_score of rf: {rf_metrics['f1_score']}")


    # y_pred_0_id3, y_test_0_id3, y_pred_1_id3, y_test_1_id3 = get_sub_predictions(y_test, y_pred_decision_tree_with_id3_model)

    # id3_0_metrics = get_metrics(y_test_0_id3, y_pred_0_id3)
    # id3_1_metrics = get_metrics(y_test_1_id3, y_pred_1_id3)

    # print("id3 - 0")
    # print(f"specificity of id3: {id3_0_metrics['specificity']}")
    # print(f"f1_score of id3: {id3_0_metrics['f1_score']}")

    # print("id3 - 1")
    # print(f"specificity of id3: {id3_1_metrics['specificity']}")
    # print(f"f1_score of id3: {id3_1_metrics['f1_score']}")

    # y_pred_0_dt, y_test_0_dt, y_pred_1_dt, y_test_1_dt = get_sub_predictions(y_test, y_pred_decision_tree_model)

    # dt_0_metrics = get_metrics(y_test_0_dt, y_pred_0_dt)
    # dt_1_metrics = get_metrics(y_test_1_dt, y_pred_1_dt)

    # print("dt - 0")
    # print(f"specificity of dt: {dt_0_metrics['specificity']}")
    # print(f"f1_score of dt: {dt_0_metrics['f1_score']}")

    # print("dt - 1")
    # print(f"specificity of dt: {dt_1_metrics['specificity']}")
    # print(f"f1_score of dt: {dt_1_metrics['f1_score']}")
    
    # y_pred_0_rf, y_test_0_rf, y_pred_1_rf, y_test_1_rf = get_sub_predictions(y_test, y_pred_random_forest_model)

    # rf_0_metrics = get_metrics(y_test_0_rf, y_pred_0_rf)
    # rf_1_metrics = get_metrics(y_test_1_rf, y_pred_1_rf)

    # print("rf - 0")
    # print(f"specificity of rf: {rf_0_metrics['specificity']}")
    # print(f"f1_score of rf: {rf_0_metrics['f1_score']}")

    # print("rf - 1")
    # print(f"specificity of rf: {rf_1_metrics['specificity']}")
    # print(f"f1_score of rf: {rf_1_metrics['f1_score']}")

    # id3_classification_report = classification_report(y_test, y_pred_decision_tree_with_id3_model)
    # dt_classification_report = classification_report(y_test, y_pred_decision_tree_model)
    # rf_classification_report = classification_report(y_test, y_pred_random_forest_model)

    # print("id3")
    # print(id3_classification_report)

    # print("dt")
    # print(dt_classification_report)

    # print("rf")
    # print(rf_classification_report)

    # print("id3")
    # print(f1_score(y_test, y_pred_decision_tree_with_id3_model))

    # print("dt")
    # print(f1_score(y_test, y_pred_decision_tree_model))

    # print("rf")
    # print(f1_score(y_test, y_pred_random_forest_model))

    # res = []
    # for l in [0,1]:
    #     prec,recall,_,_ = precision_recall_fscore_support(np.array(y_test)==l,
    #                                                     np.array(y_pred_decision_tree_with_id3_model)==l,
    #                                                     pos_label=True,average=None)
    #     res.append([l,recall[0],recall[1]])
    
    # print(pd.DataFrame(res,columns = ['class','sensitivity','specificity']))

    # res = []
    # for l in [0,1]:
    #     prec,recall,_,_ = precision_recall_fscore_support(np.array(y_test)==l,
    #                                                     np.array(y_pred_decision_tree_model)==l,
    #                                                     pos_label=True,average=None)
    #     res.append([l,recall[0],recall[1]])
    
    # print(pd.DataFrame(res,columns = ['class','sensitivity','specificity']))

    # res = []
    # for l in [0,1]:
    #     prec,recall,_,_ = precision_recall_fscore_support(np.array(y_test)==l,
    #                                                     np.array(y_pred_random_forest_model)==l,
    #                                                     pos_label=True,average=None)
    #     res.append([l,recall[0],recall[1]])
    
    # print(pd.DataFrame(res,columns = ['class','sensitivity','specificity']))

    n_tests = 10

    # summation = 0
    # for index in range(n_tests):
    #     id3 = DT_with_ID3.DecisionTree(max_depth=n_tests)
    #     start = time()
    #     id3.fit(X_train, y_train)
    #     finish = time()

    #     duration = finish - start
    #     summation += duration
    # average_training_duration = summation / n_tests
    # print(f"fitting id3 took on average: {average_training_duration} seconds")

    # summation = 0
    # for index in range(n_tests):
    #     dt = Decision_tree.DecisionTree(max_depth=n_tests)
    #     start = time()
    #     dt.fit(X_train, y_train)
    #     finish = time()

    #     duration = finish - start
    #     summation += duration
    # average_training_duration = summation / n_tests
    # print(f"fitting dt took on average: {average_training_duration} seconds")
    

    # summation = 0
    # for index in range(n_tests):
    #     rf = Random_forest.RandomForest(n_trees=15)
    #     start = time()
    #     dt.fit(X_train, y_train)
    #     finish = time()

    #     duration = finish - start
    #     summation += duration
    # average_training_duration = summation / n_tests
    # print(f"fitting rf took on average: {average_training_duration} seconds")

    for trials in range(3):
        summation = 0
        for index in range(n_tests):
            start = time()
            decision_tree_with_id3_model.predict(X_test)
            finish = time()

            duration = finish - start
            summation += duration
        average_prediction_duration = summation / n_tests
        print(f"prediction using id3 took on average: {average_prediction_duration} seconds")

        summation = 0
        for index in range(n_tests):
            start = time()
            decision_tree_model.predict(X_test)
            finish = time()

            duration = finish - start
            summation += duration
        average_prediction_duration = summation / n_tests
        print(f"prediction using dt took on average: {average_prediction_duration} seconds")

        summation = 0
        for index in range(n_tests):
            start = time()
            random_forest_model.predict(X_test)
            finish = time()

            duration = finish - start
            summation += duration
        average_prediction_duration = summation / n_tests
        print(f"prediction using rf took on average: {average_prediction_duration} seconds\n\n")

if __name__ == "__main__":
    main()