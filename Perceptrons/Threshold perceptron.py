# Author: Mikita Zyhmantovich
# Threshold perceptron
import random
import itertools
import numpy as np
from sklearn.metrics import accuracy_score

rng = np.random.default_rng(123)

threshold = lambda x: 1 if x > 0 else 0


class Perceptron:
    def __init__(self, ninp, activation=threshold):
        self.ninp = ninp
        self.weights = rng.random(ninp + 1)
        self.activation = activation

    def out(self, xs):
        S = self.weights[1:].dot(xs) + self.weights[0]
        o = self.activation(S)
        return o

    def train(self, trainset):
        eta = 0.7
        maxiter = 100
        L = len(trainset)
        while maxiter > 0:
            oldweights = np.copy(self.weights)
            for digit in rng.permutation(range(L)):
                T = digit
                I = list(itertools.chain.from_iterable(random.choice(trainset[digit])))
                R = self.out(I)
                if T != R:
                    self.weights[0] = self.weights[0] + eta * (T - R)
                    for i in range(1, len(self.weights)):
                        self.weights[i] = self.weights[i] + eta * (T - R) * I[i-1]
            if maxiter % 10 == 0:
                print(f"new weights {self.weights}")

            if set(oldweights) == set(self.weights):
                return self.weights
            maxiter = maxiter - 1
        return self.weights

    def measure(self, test_set):
        predicted = []
        truth = []
        for digit in range(2):
            for sample in range(len(test_set[digit])):
                output = self.out(list(itertools.chain.from_iterable(test_set[digit][sample])))
                target = digit
                truth.append(target)
                predicted.append(output)
        return accuracy_score(truth, predicted)


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
                    new_digit[i][j] = ideal[key][i][j] + np.random.normal(0, 0.5)  # add normalized noise
            data[key].append(new_digit)
    return data


digits_classifier = Perceptron(16)
train_dataset = create_dataset(90)
test_dataset = create_dataset(10)
digits_classifier.train(train_dataset)
accuracy = digits_classifier.measure(test_dataset)
print(f"Test accuracy is: {accuracy * 100}%")


