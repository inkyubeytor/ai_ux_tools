# class for abstracting comparators
from typing import List
import numpy as np
from dataset.dataset import Dataset, Element


class Comparator:
    """
    Abstract class for comparators.
    """

    def __init__(self, dataset: Dataset) -> None:
        """
        Construct a new summarizer with the given dataset.
        :param dataset: The dataset to summarize.
        """
        self.dataset = dataset

    def compute_difference(self, elt1: Element, elt2: Element) -> float:
        """
        Compute a (nonnegative) difference score between 2 elements.
        :param elt1: The first element to compare.
        :param elt2: The second element to compare.
        :return: A difference score as a float.
        """
        raise NotImplementedError

    def compute_matrix(self, elt_list: List[Element]) -> np.ndarray:
        """
        Return a matrix of pairwise difference scores between elements.
        :param elt_list: The list of elements to compute over.
        :return: The upper-triangular numpy 2D array with all comparison values,
        with the diagonal zeroed.
        """
        n = len(elt_list)
        out = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                out[i, j] = self.compute_difference(elt_list[i], elt_list[j])
        return np.triu(out, 1)
