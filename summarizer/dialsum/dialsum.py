from dataset.dataset import Element
from summarizer.summarizer import Summarizer


class DialSumSummarizer(Summarizer):
    """
    Uses the DialSum model to summarize text.
    """

    # TODO: Implement element summarization.
    def summarize_element(self, element: Element) -> str:
        """
        Summarizes a single element.
        :param element: An element from the dataset.
        :return: A summary of the input.
        """
        raise NotImplementedError
