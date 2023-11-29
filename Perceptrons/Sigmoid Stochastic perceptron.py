import random
import itertools
import numpy as np
import math
from sklearn.metrics import accuracy_score

rng = np.random.default_rng(123)

sigmoid = lambda x: 1 / (1 + math.e ** -x)


class Perceptron:
    def __init__(self, ninp, activation=sigmoid):
        self.ninp = ninp
        self.weights = rng.random(ninp + 1)
        for i in range(ninp + 1):
            self.weights[i] /= 10
        self.activation = activation

    def out(self, xs):
        S = self.weights[1:].dot(xs) + self.weights[0]
        o = self.activation(S)
        return o

    def train(self, trainset, batch_size=1):
        eta = 0.5
        maxiter = 100
        while maxiter > 0:
            oldweights = np.copy(self.weights)
            delta = [0 for _ in range(len(self.weights))]
            for _ in range(batch_size):
                T = random.choice(list(trainset.keys()))
                I = list(itertools.chain.from_iterable(random.choice(trainset[T])))
                R = self.out(I)
                delta[0] = self.weights[0] + eta * (T - R) * R * (1 - R)
                for i in range(1, len(delta)):
                    delta[i] += eta * (T - R) * R * (1 - R) * I[i-1]
            for i in range(len(self.weights)):
                self.weights[i] += delta[i]
            if maxiter % 10 == 0:
                print(f"new weights {self.weights}")

            if (oldweights == self.weights).all:
                return self.weights
            maxiter = maxiter - 1
        return self.weights

    def measure(self, test_set):
        predicted = []
        truth = []
        for digit in range(2):
            for sample in range(len(test_set[digit])):
                b = self.out(list(itertools.chain.from_iterable(test_set[digit][sample])))
                output = round(b)
                target = digit
                # print(f"Predicted: {output} \n Truth: {target}")
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
    for _ in range(size - 2):
        for key in ideal.keys():
            new_digit = [[0 for _ in range(4)] for _ in range(4)]
            for i in range(4):
                for j in range(4):
                    new_digit[i][j] = ideal[key][i][j] + np.random.normal(0, 0.5)
            data[key].append(new_digit)
    return data


digits_classifier = Perceptron(16)
train_dataset = create_dataset(90)
test_dataset = create_dataset(10)
digits_classifier.train(train_dataset)
accuracy = digits_classifier.measure(test_dataset)
print(f"Test accuracy is: {accuracy * 100}%")


