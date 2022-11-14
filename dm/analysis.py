import pandas as pd
from matplotlib import pyplot as plt
from collections import Counter
import math
import numpy as np

with open("dataset.xlsx", "rb") as file:
    file_content = file.read()

df = pd.read_excel(file_content)


def find_median(sequence):
    sequence = sorted(sequence)
    sequence_length = len(sequence)
    if sequence_length % 2 == 0:
        center = round(sequence_length / 2)
        mediane = (sequence[center - 1] + sequence[center]) / 2
        return (center - 1, center), mediane
    else:
        center = round((sequence_length + 1) / 2)
        mediane = sequence[center - 1]
        return (center - 1, None), mediane


def quartiles(sequence):
    sequence = sorted(sequence)

    q0 = sequence[0]
    q4 = sequence[-1]

    sequence_length = len(sequence)

    if sequence_length % 2 == 0:
        (index_1, index_2), q2 = find_median(sequence)
        _, q1 = find_median(sequence[:round(index_1) + 1])
        _, q3 = find_median(sequence[round(index_2):])
        return q0, q1, q2, q3, q4
    else:
        (index_1, _), q2 = find_median(sequence)
        _, q1 = find_median(sequence[:round(index_1)])
        _, q3 = find_median(sequence[round(index_1) + 1:])
        return q0, q1, q2, q3, q4


def find_outliers(sequence):
    _, q1, _, q3, _ = quartiles(sequence)
    iqr = q3 - q1
    outliers = [index for index, value in enumerate(sequence)
                if value > q3 + iqr * 1.5 or value < q1 - iqr * 1.5]
    return outliers


def find_mean(sequence):
    sequence_length = len(sequence)
    if not sequence_length:
        raise ValueError("Empty Sequence")

    summation = sum(sequence)
    return summation / sequence_length


def find_modes(sequence):
    if sequence.empty:
        return []
    sequence_counter = Counter(sequence)

    _, maximum_frequency = sequence_counter.most_common(1)[0]
    modes = [k for k, v in sequence_counter.items() if v == maximum_frequency]

    return modes


def symmetry(sequence):
    epsilon = 0.1
    sequence_mean = find_mean(sequence)
    _, sequence_median = find_median(sequence)
    sequence_modes = find_modes(sequence)
    sequence_mode = sequence_modes[0]

    if abs(sequence_median - sequence_mean) < epsilon and abs(sequence_median - sequence_mode) < epsilon:
        return 0  # symetrique

    if sequence_mean > sequence_median > sequence_mode:
        return 1  # symetrique positive

    if sequence_mean < sequence_median < sequence_mode:
        return -1  # symetrique negative

    return -2  # non-symetrique


def pearson_correlation(sequence_1, sequence_2):
    length_sequence_1 = len(sequence_1)
    length_sequence_2 = len(sequence_2)

    if length_sequence_1 != length_sequence_2:
        raise ValueError("Sequences of different size")

    N = length_sequence_2

    mean_sequence_1 = find_mean(sequence_1)
    mean_sequence_2 = find_mean(sequence_2)

    summation_std_sequence_1 = sum([(value - mean_sequence_1) ** 2 for value in sequence_1])
    std_sequence_1 = math.sqrt(summation_std_sequence_1 / length_sequence_1)

    summation_std_sequence_2 = sum([(value - mean_sequence_2) ** 2 for value in sequence_2])
    std_sequence_2 = math.sqrt(summation_std_sequence_2 / length_sequence_2)

    term_1 = sum([x * y for x, y in zip(sequence_1, sequence_2)])

    term_2 = N * mean_sequence_1 * mean_sequence_2

    term_3 = (N - 1) * std_sequence_1 * std_sequence_2

    try:
        return (term_1 - term_2) / term_3
    except Exception:
        return 0


def chi2(sequence_1, sequence_2):
    length_sequence_1 = len(sequence_1)
    length_sequence_2 = len(sequence_2)

    if length_sequence_1 != length_sequence_2:
        raise ValueError("Sequences of different size")

    unique_sequence_1 = sorted(set(sequence_1))
    unique_sequence_2 = sorted(set(sequence_2))

    n_unique_sequence_1 = len(unique_sequence_1)
    n_unique_sequence_2 = len(unique_sequence_2)

    matrix = np.zeros((n_unique_sequence_1, n_unique_sequence_2))

    for element_sequence_1, element_sequence_2 in zip(sequence_1, sequence_2):
        matrix[element_sequence_1, element_sequence_2] += 1

    summation = 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            observed = matrix[i, j]
            expected = (matrix[i].sum() * matrix[:, j].sum()) / matrix.sum()
            summation += (observed - expected) ** 2 / expected

    return summation


def encode(sequence):
    sequence_unique_values = set(sequence)
    sequence_unique_values_dictionary = {value: index for index, value in enumerate(sequence_unique_values)}
    encoding = [sequence_unique_values_dictionary[value] for value in sequence]
    return encoding


def attribute_type(dataset, attribute):
    n_unique = dataset[attribute].nunique()

    if dataset[attribute].dtype == "object":
        return ["discret", "nominal"]

    if n_unique > 9:
        return ["continue"]

    return ["discret", "ordinal"]


if __name__ == "__main__":
    pass