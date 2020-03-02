# Class for abstracting summarizers.
from typing import List

from dataset.dataset import Dataset, Element
from summarizer.frequency import FrequencySummarizer
from summarizer.summarizer_lib import save


class Summarizer:
    """
    Abstract class for summarizers.
    """

    def __init__(self, dataset: Dataset) -> None:
        """
        Construct a new summarizer with the given dataset.
        :param dataset: The dataset to summarize.
        """
        self.dataset = dataset

    def summarize_element(self, element: Element) -> str:
        """
        Summarizes a single element.
        :param element: An element from the dataset.
        :return: A summary of the input.
        """
        raise NotImplementedError

    def summarize_document(self, document_name: str, fp: str = None) \
            -> List[str]:
        """
        Summarize all elements in a document.
        :param document_name: The name of the document to summarize.
        :param fp: The filepath to write the output to. Default None.
        :return: A list of summaries for each element in the dataset.
        """
        document = self.dataset.retrieve_document(document_name)
        summaries = [self.summarize_element(e) for e in document]
        if fp is not None:
            save(document, summaries, fp)
        return summaries

    def summarize_dataset(self, fp: str) -> None:
        """
        Summarizes all documents in a dataset and saves results to dir.
        :param fp: The directory to save results to.
        :return: None
        """
        for d in self.dataset.list_documents():
            self.summarize_document(d, f"{fp}/{d}")


summarizers = {
    "frequency": FrequencySummarizer
}
