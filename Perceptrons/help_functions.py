# Author: Mikita Zyhmantovich
# Supporting functions for perceptrons
import numpy as np


def create_dataset(size):
    ideal = {}
    ideal[0] = [[0, 1, 1, 0],
                [1, 0, 0, 1],
                [1, 0, 0, 1],
                [0, 1, 1, 0]]
    ideal[1] = [[0, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]]
    data = {0: [ideal[0]], 1: [ideal[1]]}
    for _ in range(size - 1):
        for key in ideal.keys():
            new_digit = [[0 for _ in range(4)] for _ in range(4)]
            for i in range(4):
                for j in range(4):
                    new_digit[i][j] = ideal[key][i][j] + np.random.normal(0, 0.5)
            data[key].append(new_digit)
    return data


def accuracy_score(truth, predicted):
    if len(truth) == len(predicted):
        predicted_right = 0
        for i in range(len(truth)):
            if truth[i] == predicted[i]:
                predicted_right += 1
        return round(predicted_right / len(truth), 2)
    return -1