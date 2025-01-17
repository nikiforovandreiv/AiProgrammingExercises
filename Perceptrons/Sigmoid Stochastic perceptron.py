# Author: Mikita Zyhmantovich
# Sigmoid perceptron
import random
import itertools
import numpy as np
import math
import help_functions as hp

rng = np.random.default_rng(123)

sigmoid = lambda x: 1 / (1 + math.e ** -x)


class Perceptron:
    def __init__(self, ninp, activation=sigmoid, iterations=500):
        self.ninp = ninp
        self.maxiter = iterations
        self.weights = rng.random(ninp + 1)
        self.activation = activation

    def out(self, xs):
        S = self.weights[1:].dot(xs) + self.weights[0]
        o = self.activation(S)
        return o

    def train(self, trainset, batch_size=1):
        eta = 0.5
        while self.maxiter > 0:
            oldweights = np.copy(self.weights)
            delta = [0 for _ in range(len(self.weights))]
            for _ in range(batch_size):
                T = random.choice(list(trainset.keys()))
                I = list(itertools.chain.from_iterable(random.choice(trainset[T])))
                R = self.out(I)
                delta[0] = eta * (T - R) * R * (1 - R)
                for i in range(1, len(delta)):
                    delta[i] = eta * (T - R) * R * (1 - R) * I[i-1]
            for i in range(len(self.weights)):
                self.weights[i] += delta[i]
            if self.maxiter % 50 == 0:
                print(f"new weights {self.weights}")

            if set(oldweights) == set(self.weights):
                return self.weights
            self.maxiter = self.maxiter - 1
        return self.weights

    def measure(self, test_set):
        predicted = []
        truth = []
        for digit in range(2):
            for sample in range(len(test_set[digit])):
                b = self.out(list(itertools.chain.from_iterable(test_set[digit][sample])))
                output = round(b)
                target = digit
                truth.append(target)
                predicted.append(output)
        return hp.accuracy_score(truth, predicted)


digits_classifier = Perceptron(16)
train_dataset = hp.create_dataset(90)
test_dataset = hp.create_dataset(10)
digits_classifier.train(train_dataset)
accuracy = digits_classifier.measure(test_dataset)
print(f"Test accuracy is: {accuracy * 100}%")
