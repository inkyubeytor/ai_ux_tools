from dataset.dataset import Element
from comparator.comparator import Comparator
from lib.preprocessing import lemmatization, cleaning
from typing import Set


class JaccardComparator(Comparator):
    """
    Comparator based on Jaccard similarity of elements.
    https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
    """

    def _lemma_set(self, elt: Element) -> Set[str]:
        """
        Returns a set of all word lemmas in an element.
        :param elt: The element to process.
        :return: A set containing lemmas for each non-stopword in an element.
        """
        sentences = self.dataset.sentence_tokenize(elt)
        sentences = cleaning.remove_punctuation(sentences)
        words = [self.dataset.word_tokenize(s) for s in sentences]
        words = [w for s in words for w in cleaning.remove_stop_words(s)]
        return set(lemmatization.lemmatize(lemmatization.pos_tag(words)))

    def compute_difference(self, elt1: Element, elt2: Element) -> float:
        """
        Computes the Jaccard distance between input elements.
        :param elt1: The first element to compare.
        :param elt2: The second element to compare.
        :return: A Jaccard distance 0 <= J <= 1, where higher indices indicate
        less similar inputs.
        """
        a, b = self._lemma_set(elt1), self._lemma_set(elt2)
        c = a.intersection(b)
        return 1 - (len(c) / (len(a) + len(b) - len(c)))
