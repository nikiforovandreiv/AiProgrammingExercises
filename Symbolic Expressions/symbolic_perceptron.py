"""
Author: Sergei Baginskii

Code for perceptron taken from the lecture notes.

For simplicity, we are only training the model for recognising 0, without the possibility of changing
training goal. Code can be easily modified to have the ability to change the goal, as in the perceptron
from the original task.
"""
import numpy as np
from language_extended import *
import data_creator


def linear(xs):
    s = Var("w0")  # bias
    for i in range(len(xs)):
        s = s + Var(f"w{i + 1}")*xs[i]
    return s


def sigmoid(xs):
    s = Var("w0")  # bias
    for i in range(len(xs)):
        s = s + Var(f"w{i + 1}") * xs[i]
    return Con(1) / (Exp(-s) + 1)


class Perceptron:
    rng = np.random.default_rng()  # random interface
    ideal_data = data_creator.create_dataset()  # ideal data for training

    def __init__(self, ninp, sigma, weights=None):
        self.dataset_size = 200
        self.ninp = ninp  # number of inputs
        self.sigma = sigma  # input vector -> symbolic expression
        self.weights = {}  # environment for parameters
        vals = weights if weights else (Perceptron.rng.random(self.ninp + 1) - 1) / 10
        for i in range(self.ninp + 1):  # ninp weights and a bias
            self.weights[f"w{i}"] = vals[i]

        # creating a dataset
        self.data = data_creator.DataCreator(Perceptron.ideal_data, self.dataset_size)
        self.dataset = self.data.dataset
        # separating the dataset into training and testing sets
        self.training_set = self.dataset[:int(self.dataset.shape[0] * 9 / 10)]  # 90% of the set for training
        self.training_targets = self.training_set[:, -1]  # separating the targets
        self.training_set = self.training_set[:, :-1]  # separating the values from the targets

        self.testing_set = self.dataset[int(self.dataset.shape[0] * 9 / 10):]  # 10% for validation
        self.testing_targets = self.testing_set[:, -1]  # separating the targets
        self.testing_set = self.testing_set[:, :-1]  # separating the values from the targets

    def output(self, inp):
        formula = self.sigma(inp)
        return formula

    def loss(self):
        err = 0
        for i in range(len(self.training_set)):
            xs = self.training_set[i]
            t = Con(self.training_targets[i])
            o = self.output(xs).ev(self.weights).simplify()
            err += ((t - o) * (t - o)).simplify().val
        return err / 2

    def partial_der(self, inputs, target, key):
        temp = ((target - self.output(inputs)) * (target - self.output(inputs))).diff(key).simplify().ev(self.weights).simplify()
        return temp

    def train(self):
        maxepoch = 1000
        batchsize = 20
        alpha = Con(1e-3)
        updates = {}
        for e in range(maxepoch):
            # populating or repopulating the updates dictionary
            for key in self.weights.keys():
                updates[key] = 0
            for _ in range(batchsize):
                # choose the element for updating
                current_elem = Perceptron.rng.integers(0, self.training_set.shape[0], 1)[0]
                curr_values = self.training_set[current_elem]
                target = Con(self.training_targets[current_elem])
                for key in self.weights.keys():
                    updates[key] -= (alpha * self.partial_der(curr_values, target, key)).simplify().val
            for w in self.weights.keys():
                self.weights[w] += updates[w]
            if e % 10 == 0: print(f"epoch{e}: loss = {self.loss()}")


if __name__ == "__main__":
    perceptron = Perceptron(ninp=16, sigma=sigmoid)
    perceptron.train()
    print(perceptron.output(np.array([0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                                     dtype=float)).ev(perceptron.weights).simplify())
