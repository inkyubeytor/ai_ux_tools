from comparator.comparator import Comparator
from dataset.dataset import Element
import os
import numpy as np
import subprocess


class FastTextComparator(Comparator):
    """
    Compares elements based on cosine similarity of word vectors.
    Uses fasttext similarity comparison from
    https://github.com/ashokc/Bow-to-Bert/blob/master/fasttext_sentence_similarity.py
    """

    # TODO: Fix grep call
    def compute_difference(self, elt1: Element, elt2: Element) -> float:
        """
        Computes the similarity of 2 elements using fasttext.
        :param elt1: The first element to compare.
        :param elt2: The second element to compare.
        :return: 1 - similarity of the inputs.
        """
        sentences = [elt1, elt2]
        words_by_sentence, words = {}, []
        for i, sentence in enumerate(sentences):
            words_by_sentence[i] = sentence.replace('\n', ' ').split(' ')
            words = words + words_by_sentence[i]

        wordVectorLength, zeroVectorCount = 300, 0
        filename = 'crawl-300d-2M-subword/crawl-300d-2M-subword.vec'
        docVectors = np.zeros((3, wordVectorLength), dtype='float32')
        for word in words:
            w = "^\"" + word + " \" "
            grep_command = 'grep ' + w + filename + ' -m 1'
            # TODO: Fix slowness of grep on words with apostrophes
            try:
                s = subprocess.check_output(grep_command,
                                            cwd="comparator/fasttext/",
                                            shell=True).decode("utf-8")
            except subprocess.CalledProcessError:
                continue
            tokens = s.rstrip().split(' ')
            wv = np.asarray(tokens[1:], dtype='float32')
            if len(wv) == wordVectorLength:
                for i in range(2):
                    if word in words_by_sentence[i]:
                        docVectors[i] = docVectors[i] + wv / np.linalg.norm(wv)
            else:
                zeroVectorCount += 1

        for i in range(2):
            docVectors[i] = docVectors[i] / np.linalg.norm(docVectors[i])
        return 1 - np.dot(docVectors[0], docVectors[1])
