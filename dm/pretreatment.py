from collections import Counter
import math
import pandas as pd
import numpy as np

from dm.analysis import attribute_type

with open("dataset.xlsx", "rb") as file:
    file_content = file.read()

df = pd.read_excel(file_content)

df.at[0, "Age"] = np.nan


def min_max_normalization(sequence, minimum, maximum):
    sequence_length = len(sequence)

    if not sequence_length:
        raise ValueError("Empty Sequence")

    minimum_value = min(sequence)
    maximum_value = max(sequence)

    maximum_value_minus_minimum_value = maximum_value - minimum_value
    maximum_minus_minimum = (maximum - minimum)

    normalized_sequence = [((value - minimum_value) / maximum_value_minus_minimum_value)
                           * maximum_minus_minimum + minimum for value in sequence]

    return normalized_sequence


def z_score_normalization(sequence):
    sequence_length = len(sequence)

    if not sequence_length:
        raise ValueError("Empty Sequence")

    # compute mean
    summation_sequence_mean = sum(sequence)
    sequence_mean = summation_sequence_mean / sequence_length

    # compute standard deviation
    summation_sequence_std = sum([(value - sequence_mean) ** 2 for value in sequence])
    sequence_std = math.sqrt(summation_sequence_std / sequence_length)

    if sequence_std == 0:
        return sequence

    # construct
    normalized_sequence = [(value - sequence_mean) / sequence_std for value in sequence]

    return normalized_sequence


def fill_mean(dataset, attribute):
    sequence = dataset[attribute]
    sequence_length = len(sequence)

    if not sequence_length:
        raise ValueError("Empty Sequence")

    summation_sequence = sum(sequence)

    mean_sequence = summation_sequence / sequence_length

    try:
        dataset[attribute].fillna(mean_sequence, inplace=True)
    except:
        pass


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


def fill_median(dataset, attribute):
    sequence = dataset[attribute]
    sequence_length = len(sequence)

    if not sequence_length:
        raise ValueError("Empty Sequence")

    _, sequence_median = find_median(sequence)

    try:
        dataset[attribute].fillna(sequence_median, inplace=True)
    except:
        pass


def fill_mode(dataset, attribute):
    sequence = dataset[attribute]
    sequence_length = len(sequence)

    if not sequence_length:
        raise ValueError("Empty Sequence")

    counter = Counter(sequence)
    sequence_mode, _ = counter.most_common(1)[0]

    try:
        dataset[attribute].fillna(sequence_mode, inplace=True)
    except:
        pass


def fill_unknown(dataset, attribute):
    sequence = dataset[attribute]
    sequence_length = len(sequence)

    if not sequence_length:
        raise ValueError("Empty Sequence")

    try:
        dataset[attribute].fillna("UNKNOWN", inplace=True)
    except:
        pass
