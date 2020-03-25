from comparator.comparator import Comparator
from dataset.dataset import Element


# TODO: Finish implementation of this
class CosineComparator(Comparator):
    """
    Compares elements based on cosine similarity of word vectors.
    https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
    """

    # def _word_vector(self, elt: Element) -> SOMETHING:

    def compute_difference(self, elt1: Element, elt2: Element) -> float:
        """
        Computes the cosine similarity of the word vectors of 2 elements.
        :param elt1: The first element to compare.
        :param elt2: The second element to compare.
        :return: 1 - cosine similarity of the inputs.
        """
        raise NotImplementedError
