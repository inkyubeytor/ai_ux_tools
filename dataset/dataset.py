# Class for abstracting handling of datasets
import os
from typing import List

from lib.preprocessing.cleaning import sentences, words

Element = str
Document = List[Element]


class Dataset:
    """
    Abstracts loading of datasets.
    """

    # General Methods

    def __init__(self, root: str) -> None:
        """
        Initialize a dataset.
        :param root: The root directory of the dataset.
        :return: None
        """
        self.root = root

    @staticmethod
    def get_size(start_path):
        """
        Gets the size of a directory recursively.
        From https://gist.github.com/SteveClement/3755572.
        :param start_path: The path to compute size of.
        :return: The size of the directory on disk.
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def dataset_info(self, fp: str = None) -> None:
        """
        Outputs information about the dataset.
        :param fp: The file path to dump information to. If None, information is
        printed to stdout.
        :return: None
        """
        raise NotImplementedError

    # Document Methods

    def list_documents(self) -> List[str]:
        """
        List all the available documents in the dataset.
        :return: A list of document names.
        """
        raise NotImplementedError

    def retrieve_document(self, document_name: str) -> Document:
        """
        Load a document from disk.
        :param document_name: The name of the document to load.
        :return: A loaded document.
        """
        raise NotImplementedError

    def kth_elements(self, k: int) -> List[Element]:
        """
        If valid, returns a list of the kth elements from each document.
        :param k: The index of the element to return.
        :return: A list of kth elements or None.
        """
        out = []
        for d in self.list_documents():
            try:
                out.append(self.retrieve_document(d)[k])
            except IndexError:
                raise IndexError(f"Element index k = {k} "
                                 f"is out of bounds for document {d}")
        return out

    # Element Methods

    @staticmethod
    def sentence_tokenize(element: Element) -> List[str]:
        """
        Split an element into sentences.
        :param element: The element to split.
        :return: A list of sentences from the element, in order.
        """
        return sentences(element)

    @staticmethod
    def word_tokenize(sentence: str) -> List[str]:
        """
        Split a sentence into words.
        :param sentence: A sentence from the dataset.
        :return: A list of words in the sentence.
        """
        return words(sentence)
