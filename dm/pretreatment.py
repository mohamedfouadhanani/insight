from collections import Counter
import math
import pandas as pd
import numpy as np

# from dm.analysis import attribute_type

with open("dataset.xlsx", "rb") as file:
    file_content = file.read()

df = pd.read_excel(file_content)

df.at[0, "Age"] = 200
df.at[5, "Age"] = 212


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
    sequence = dataset[dataset[attribute].notna()][attribute]
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
    sequence = dataset[dataset[attribute].notna()][attribute]
    sequence_length = len(sequence)

    if not sequence_length:
        raise ValueError("Empty Sequence")

    _, sequence_median = find_median(sequence)

    try:
        dataset[attribute].fillna(sequence_median, inplace=True)
    except:
        pass


def fill_mode(dataset, attribute):
    sequence = dataset[dataset[attribute].notna()][attribute]
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
    sequence = dataset[dataset[attribute].notna()][attribute]
    sequence_length = len(sequence)

    if not sequence_length:
        raise ValueError("Empty Sequence")

    try:
        dataset[attribute].fillna("UNKNOWN", inplace=True)
    except:
        pass


def fill_minimum(dataset, attribute):
    sequence = dataset[dataset[attribute].notna()][attribute]
    sequence_length = len(sequence)

    if not sequence_length:
        raise ValueError("Empty Sequence")

    minimum = sequence.min()
    try:
        dataset[attribute].fillna(minimum, inplace=True)
    except:
        pass


def equal_intervals_discretization(dataset, attribute, k):
    if dataset[attribute].isna().sum() > 0:
        raise ValueError("NaN Value")

    minimum = dataset[attribute].min()
    maximum = dataset[attribute].max()
    n = len(dataset[attribute])

    # k = (1 + 3 * np.log10(n)).astype(int)

    length = (maximum - minimum) / k

    intervals = []
    for _ in range(k):
        intervals.append([])

    for value in dataset[attribute]:
        a = minimum
        b = minimum + length
        j = 0

        found = False
        while not found:
            if value == maximum:
                intervals[len(intervals) - 1].append(value)
                found = True

                break
            if a <= value and value < b:
                intervals[j].append(value)
                found = True

                break
            else:
                a += length
                b += length
                j += 1

    for index, value in enumerate(dataset[attribute]):
        for interval in intervals:
            if value in interval:
                mean = sum(interval) / len(interval)
                dataset.at[index, attribute] = mean
                break


def quantile_discretization(dataset, attribute, k):
    if dataset[attribute].isna().sum() > 0:
        raise ValueError("NaN Value")

    sequence = sorted(dataset[attribute].unique())

    a = len(sequence)
    n = int(a / k)

    intervals = []
    for i in range(0, k):
        interval = []
        for j in range(i * n, (i + 1) * n):
            if j >= a:
                break
            interval.append(sequence[j])
        intervals.append(interval)

    for index, value in enumerate(dataset[attribute]):
        for interval in intervals:
            if value in interval:
                mean = sum(interval) / len(interval)
                dataset.at[index, attribute] = mean
                break


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


def remove_outliers_quantile_discretization(dataset, attribute, k):
    if dataset[attribute].isna().sum() > 0:
        raise ValueError("NaN Value")

    sequence = sorted(dataset[attribute].unique())

    a = len(sequence)
    n = int(a / k)

    intervals = []
    for i in range(0, k):
        interval = []
        for j in range(i * n, (i + 1) * n):
            if j >= a:
                break
            interval.append(sequence[j])
        intervals.append(interval)

    outlier_indices = find_outliers(dataset[attribute])

    for index in outlier_indices:
        value = dataset[attribute][index]

        for interval in intervals:
            if value in interval:
                mean = round(sum(interval) / len(interval))

                print(f"value {value} is replaced with {mean} because of the interval {interval}")

                dataset.at[index, attribute] = mean
                break


def remove_outliers_equal_intervals_discretization(dataset, attribute, k):
    if dataset[attribute].isna().sum() > 0:
        raise ValueError("NaN Value")

    minimum = dataset[attribute].min()
    maximum = dataset[attribute].max()
    n = len(dataset[attribute])

    # k = (1 + 3 * np.log10(n)).astype(int)

    length = (maximum - minimum) / k

    intervals = []
    for _ in range(k):
        intervals.append([])

    for value in dataset[attribute]:
        a = minimum
        b = minimum + length
        j = 0

        found = False
        while not found:
            if value == maximum:
                intervals[len(intervals) - 1].append(value)
                found = True

                break
            if a <= value and value < b:
                intervals[j].append(value)
                found = True

                break
            else:
                a += length
                b += length
                j += 1

    outlier_indices = find_outliers(dataset[attribute])

    for index in outlier_indices:
        value = dataset[attribute][index]

        for interval in intervals:
            if value in interval:
                mean = round(sum(interval) / len(interval))

                dataset.at[index, attribute] = mean
                break
