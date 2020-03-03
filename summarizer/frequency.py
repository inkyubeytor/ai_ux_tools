from dataset.dataset import Dataset, Element
from preprocessing import cleaning, lemmatization, analysis
from summarizer.summarizer import Summarizer


class FrequencySummarizer(Summarizer):
    """
    Simple summarizer based on word frequencies.
    """

    def __init__(self, dataset: Dataset) -> None:
        """
        Construct a new summarizer with the given dataset.
        :param dataset: The dataset to summarize.
        """
        super().__init__(dataset)

    def summarize_element(self, element: Element, threshold: float = 1.5) \
            -> str:
        """
        Perform extractive text summarization on an input text.
        :param element: A text element to summarize.
        :param threshold: The relative score threshold for the inclusion of a
        sentence in a summary.
        :return: An extractive text summarization.
        """
        # Convert sentences into lists of words.
        sentences = self.dataset.sentence_tokenize(element)
        sentences = cleaning.remove_punctuation(sentences)
        words = [self.dataset.word_tokenize(s) for s in sentences]
        words = [cleaning.remove_stop_words(s) for s in words]

        # Use POS tagging to lemmatize input.
        lemmas = [lemmatization.lemmatize(lemmatization.pos_tag(s)) for s in
                  words]

        # Compute sentence scores based on frequency.
        table = analysis.frequency_table([word for s in lemmas for word in s])
        scores = [(sum(table[w] for w in s) / len(s)) if len(s) > 0 else 0
                  for s in lemmas]
        score_threshold = threshold * sum(scores) / len(scores)

        # Add highest scoring sentences to summary.
        summary = ""
        for sentence, score in zip(sentences, scores):
            if score > score_threshold:
                summary += sentence
        return summary
