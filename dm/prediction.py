import numpy as np

def confusion_matrix(observed, expected):
    if not observed:
        raise ValueError("observed is an empty list")
    
    if not expected:
        raise ValueError("expected is an empty list")

    observed_length = len(observed)
    expected_length = len(expected)

    if observed_length != expected_length:
        raise ValueError("different lengths")
    
    confusion_counter = [[0, 0], [0, 0]]
    for o, e in zip(observed, expected):
        confusion_counter[o][e] += 1
    
    return confusion_counter


def accuracy(confusion_matrix):
    TN = confusion_matrix[0][0]
    FN = confusion_matrix[0][1]
    FP = confusion_matrix[1][0]
    TP = confusion_matrix[1][1]

    result = (TP + TN) / (TP + TN + FP + FN)
    return result

def precision(confusion_matrix):
    FP = confusion_matrix[1][0]
    TP = confusion_matrix[1][1]

    result = TP / (TP + FP)
    return result

def recall(confusion_matrix):
    TN = confusion_matrix[0][0]
    FN = confusion_matrix[0][1]
    FP = confusion_matrix[1][0]
    TP = confusion_matrix[1][1]

    result = TP / (TP + FN)
    return result

def recall(precision, recall):
    result = 2 * precision * recall / (precision + recall)
    return result

def train_test_split(dataframe):
    mask = np.random.rand(len(dataframe)) < 0.8

    train = dataframe[mask]
    test = dataframe[~mask]

    return train, test