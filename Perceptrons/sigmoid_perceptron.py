"""
Author: Sergei Baginskii

Both my versions of perceptrons have the precision of 100%.
"""
import numpy as np
import data_creator


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Perceptron:
    # random interface
    rng = np.random.default_rng()

    # data of ideally looking numbers
    ideal_data = data_creator.create_dataset()

    def __init__(self, goal, activation_func=sigmoid):
        # constants
        self.dataset_size = 100

        # variables
        self.goal = goal  # which number are we training our perceptron for
        self.activation = activation_func
        self.data = data_creator.DataCreator(Perceptron.ideal_data, self.dataset_size)
        self.num_inputs = self.data.dimensions[0] * self.data.dimensions[1]  # number of variables
        self.weights = Perceptron.rng.random(self.num_inputs + 1)

        self.dataset = self.data.dataset
        self.modify_targets()  # changes targets from numbers (0, 1, 2, ...) to 0 / 1

        Perceptron.rng.shuffle(self.dataset)  # randomize the order of elements in the dataset
        self.training_set = self.dataset[:int(self.dataset.shape[0] * 9 / 10)]  # 90% of the set for training
        self.testing_set = self.dataset[int(self.dataset.shape[0] * 9 / 10):]  # 10% for validation

    def output(self, values):
        aggregation = values.dot(self.weights[1:]) - self.weights[0]
        result = self.activation(aggregation)
        return result

    def train(self):
        eta = 0.1  # training constant
        maxiter = 1000
        targets = self.training_set.T[-1]
        trainset = self.training_set.T[:-1]
        trainset = trainset.T
        for i in range(maxiter):
            delta = np.zeros(np.shape(self.weights)[0])
            batch_size = targets.shape[0]
            oldweights = np.copy(self.weights)
            for _ in range(10):
                current_elem = Perceptron.rng.integers(0, batch_size, 1)[0]
                curr_values = trainset[current_elem]
                result = self.output(curr_values)
                target = targets[current_elem]
                delta[0] += eta * (target - result) * result * (1 - result)
                delta[1:] += eta * (target - result) * result * (1 - result) * curr_values
            self.weights += delta

            if i % 100 == 0:
                print(f"Current weights {self.weights}")

            if np.all(oldweights == self.weights):
                break

        return self.weights

    def modify_targets(self):
        """
        Since our targets in out dataset represent numbers, we change any number to 0 if a number is not out target
        or to 1 if it is a target
        """
        self.dataset = self.dataset.T
        for i in range(self.dataset.shape[1]):
            if self.dataset[-1][i] != self.goal:
                self.dataset[-1][i] = 0
            else:
                self.dataset[-1][i] = 1
        self.dataset = self.dataset.T

    def check_train(self):
        targets = self.testing_set.T[-1]
        testset = self.testing_set.T[:-1]
        testset = testset.T
        hits = 0
        totals = 0
        for i in range(testset.shape[0]):
            result = self.output(testset[i])
            if abs(result - targets[i]) < 0.5:  # we check if the result is closer to being correct than incorrect
                hits += 1
            totals += 1
        print(f'Precision is {hits / totals * 100}%')


if __name__ == "__main__":
    perceptron = Perceptron(goal=4)
    perceptron.train()
    perceptron.check_train()
