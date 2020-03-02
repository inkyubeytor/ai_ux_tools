# Class for abstracting handling of datasets
from typing import List

from dataset.blogger import BloggerDataset

Element = str
Document = List[Element]


class Dataset:
    """
    Abstracts loading of datasets.
    """

    def __init__(self, root: str) -> None:
        """
        Initialize a dataset.
        :param root: The root directory of the dataset.
        :return: None
        """
        self.root = root

    def dataset_info(self, fp: str = None) -> None:
        """
        Outputs information about the dataset.
        :param fp: The file path to dump information to. If None, information is
        printed to stdout.
        :return: None
        """
        raise NotImplementedError

    # Document methods

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

    # TODO: Implement element-specific methods for tokenization, etc.


datasets = {
    "blogs": BloggerDataset
}
