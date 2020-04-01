from dataset.dataset import Element
from summarizer.summarizer import Summarizer
import summa


class TextRankSummarizer(Summarizer):
    """
    Textrank-based extractive summarizer using the `summa` library.
    https://pypi.org/project/summa/
    """

    def summarize_element(self, element: Element, ratio: float = 0.3) \
            -> str:
        """
        Perform text summarization on an input text.
        :param element: A text element to summarize.
        :param ratio: The approximate length of the summary relative to the
        input length.
        :return: An extractive text summarization.
        """
        # Convert sentences into lists of words.
        sentences = self.dataset.sentence_tokenize(element)
        in_data = '\n'.join(sentences)
        return summa.summarizer.summarize(in_data, ratio=ratio)
