from comparator.comparator import Comparator
from dataset.dataset import Element
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np


class CosineComparator(Comparator):
    """
    Compares elements based on cosine similarity of word vectors.
    Uses sklearn-based cosine similarity.
    https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
    """

    def compute_difference(self, elt1: Element, elt2: Element) -> float:
        """
        Computes the cosine similarity of the word vectors of 2 elements.
        :param elt1: The first element to compare.
        :param elt2: The second element to compare.
        :return: 1 - cosine similarity of the inputs.
        """
        text = [elt1, elt2]
        vectorizer = CountVectorizer(text)
        vectorizer.fit(text)
        vectors = vectorizer.transform(text).toarray()
        vectors = normalize(vectors, norm='l2')
        return 1.0 - np.dot(vectors[0], vectors[1])
