"""
Author: Sergei Baginskii

This creates a dataset of following format:
((dim_1, dim_2), dataset[[data1_1, ..., data_1_n, current_number],
                         [data2_1, ..., data2_n, result_2], ... ]).

dim_1, dim_2 are dimensions of the digit image and helps with several calculations.
"""
import numpy as np


def create_dataset():
    dimensions = (4, 4)

    # for simplicity, the numbers are stored in flattened 2-dim arrays.
    ideal_0 = np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1], dtype=float)
    ideal_1 = np.array([0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0], dtype=float)
    ideal_nums = np.array([ideal_0, ideal_1])

    data_input = (dimensions, ideal_nums)
    return data_input


class DataCreator:
    """
    Creates a dataset of needed size and applies normally distributed noise to it.
    """
    def __init__(self, objects, dataset_size):
        # rng interface
        self.rng = np.random.default_rng()

        # variables
        self._dimensions = objects[0]
        self.ideal_data = objects[1]
        self.num_ideal_objects = len(self.ideal_data)
        self.dataset_size = dataset_size

        # containers
        self._dataset = np.empty((self.dataset_size, self._dimensions[0] * self._dimensions[1] + 1))

        # methods
        self.create_dataset()
        self.apply_noise()

    def create_dataset(self):
        """
        We populate the dataset with the roughly same number of every type of the element.
        """
        for i in range(0, self.dataset_size):
            self._dataset[i] = self.ideal_data[i % self.num_ideal_objects]

    def apply_noise(self):
        """
        Applies uniformly distributed noise to our dataset.

        Since we want to access all the elements except last ones in each row, it is faster to transpose the
        dataset and access every element except those in the last row.
        """
        self._dataset = self._dataset.T
        shape = np.shape(self._dataset)
        for i in range(shape[0] - 1):
            for j in range(shape[1]):
                noise = 0.5 * self.rng.random()
                self._dataset[i][j] += noise
        self._dataset = self._dataset.T

    @property
    def dataset(self):
        return self._dataset

    @property
    def dimensions(self):
        return self._dimensions


if __name__ == "__main__":
    data_cells = create_dataset()
    data_size = 100

    dataset_creator = DataCreator(data_cells, data_size)
    print(dataset_creator.dataset)
