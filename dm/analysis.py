import pandas as pd
from matplotlib import pyplot as plt
from collections import Counter

with open("dataset.xlsx", "rb") as file:
    file_content = file.read()

df = pd.read_excel(file_content)
# print(df)


def find_median(sequence):
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
    sequence_counter = Counter(sequence)

    _, maximum_frequency = sequence_counter.most_common(1)[0]
    modes = [k for k, v in sequence_counter.items() if v == maximum_frequency]

    return modes


def summetry(sequence):
    sequence_mean = find_mean(sequence)
    _, sequence_median = find_median(sequence)
    sequence_modes = find_modes(sequence)
    sequence_mode = sequence_modes[0]

    if sequence_mean > sequence_median > sequence_mode:
        return 1

    if sequence_mean < sequence_median < sequence_mode:
        return -1

    return 0

# q0, q1, q2, q3, q4 = quartiles([98, 90, 70, 18, 92, 92, 55, 83, 45, 95, 88, 76])
# q0, q1, q2, q3, q4 = quartiles([98, 90, 70, 18, 92, 92, 55, 83, 45, 95, 88])
# print(q0, q1, q2, q3, q4)

# print(find_outliers([98, 90, 70, 18, 92, 92, 55, 83, 45, 95, 88, 76]))
# print(find_outliers([98, 90, 70, 18, 92, 92, 55, 83, 45, 95, 88]))

# n_bins = 4
# plt.hist([98, 90, 70, 18, 92, 92, 55, 83, 45, 95, 88, 76], bins=n_bins)
# plt.xlabel("Bins")
# plt.ylabel("Frequency")
# plt.title(f"Histogram of attribute")
# plt.show()

# print(find_mode([1, 1, 2, 2, 1, 2, 2, 3, 3, 4, 3, 4, 4]))
# print(find_mode([98, 90, 70, 18, 92, 92, 55, 83, 45, 95, 88]))


# print(summetry([1, 1, 2, 2, 1, 2, 2, 3, 3, 4, 3, 4, 4]))

# print(df["Attrition"].dtype)
# print(df["DailyRate"].dtype)

# print(df.iloc[[1, 2, 3]])

# for row in df["Age"]:
#     print(row)

# plt.hist(df["Age"], bins=5)
# plt.show()
