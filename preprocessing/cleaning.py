import string
from typing import List, Union

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

Text = Union[str, List[str]]


def sentences(text: str) -> List[str]:
    """
    Breaks text into sentences.
    :param text: The input text to split.
    :return: A list of all sentences in the input text.
    """
    return sent_tokenize(text)


def words(text: str) -> List[str]:
    """
    Breaks text into words.
    :param text: The input text to split.
    :return: A list of all words in the input text.
    """
    return word_tokenize(text)


def remove_punctuation(text: Text) -> Text:
    """
    Removes the punctuation from given text.
    :param text: The text to clean.
    :return: The input text without punctuation.
    """
    if type(text) is str:
        return text.translate(str.maketrans('', '', string.punctuation))
    else:
        return [t.translate(str.maketrans('', '', string.punctuation))
                for t in text]


def remove_stop_words(tokens: List[str]) -> List[str]:
    """
    Removes the stop words from a list of word tokens.
    :param tokens: The text to clean.
    :return: The input text without stop words.
    """
    return [t for t in tokens if t not in stopwords.words('english')]
