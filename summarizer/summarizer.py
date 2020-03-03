# Class for abstracting summarizers.
from typing import List

from dataset.dataset import Dataset, Element
from lib import json_tools as jtools
from summarizer.frequency import FrequencySummarizer


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

    @staticmethod
    def save(raw: List[str], summary: List[str], fp: str) -> None:
        """
        Saves document summary data to json file.
        :param raw: The input data to the summarizer.
        :param summary: The computed summary.
        :param fp: The path to save the data to.
        :return: None
        """
        data = {i: {"input": raw[i], "output": summary[i]}
                for i in range(len(raw))}
        jtools.write_to_file(fp, data)

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
            self.save(document, summaries, fp)
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
