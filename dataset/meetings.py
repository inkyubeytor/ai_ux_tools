# AMI Meetings Corpus http://groups.inf.ed.ac.uk/ami/download/
# AMI automatic annotations v1.5.1: PlainText-format directory
from typing import List
import os

from dataset.dataset import Dataset, Document, Element


class AMIDataset(Dataset):
    """
    AMI meeting corpus data.
    """

    # General Methods

    def __init__(self, root: str) -> None:
        """
        Initialize AMI Meeting Corpus dataset.
        :param root: The root directory of the dataset.
        :return: None
        """
        super().__init__(root)
        self.data = f"{self.root}/AutomaticTopicSegmentation"
        self.labels = f"{self.root}/ExtractiveSummaries"

    def dataset_info(self, fp: str = None) -> str:
        # TODO: make output json formatted.
        """
        Displays information about the meetings dataset.
        :param fp: The file path to dump information to. If None, information is
        printed to stdout.
        :return: The dataset summary as a string.
        """
        data = "AMI Meeting Corpus\n"
        data += f"Number of files: {len(os.listdir(self.data))}\n"
        data += f"Directory size: {self.get_size(self.root)}\n"
        if fp is not None:
            with open(fp, "w+") as f:
                f.write(data)
        return data

    # Document Methods

    def list_documents(self) -> List[str]:
        """
        List all the available documents in the dataset.
        :return: A list of document names.
        """
        files = os.listdir(self.data)
        files.remove("00README.txt")
        return files

    def retrieve_document(self, document_name: str) -> Document:
        """
        Load a document from disk.
        :param document_name: The name of the document to load.
        :return: A loaded document.
        """
        with open(f"{self.data}/{document_name}") as f:
            lines = [line.replace('\n', ' ') for line in f.readlines()
                     if line[0] != '#' and len(line) > 0]
        return ['\n'.join([line.split('\t')[2] for line in lines])]

    # Element Methods

    @staticmethod
    def sentence_tokenize(element: Element) -> List[str]:
        """
        Split a meeting element into sentences.
        :param element: The element to split.
        :return: A list of sentences from the element, in order.
        """
        return element.split('\n')
