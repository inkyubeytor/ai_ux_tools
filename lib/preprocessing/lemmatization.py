from typing import List, Tuple

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import nltk


def pos_tag(text: List[str]) -> List[Tuple[str, str]]:
    """
    Returns tuples associating input words with their parts of speech.
    :param text: The text to tag.
    :return: A list of the input text with the POS tags for each word.
    """
    return nltk.pos_tag(text)


def lemmatize(tagged_words: List[Tuple[str, str]], lower: bool = True) \
        -> List[str]:
    """
    Lemmatizes pos_tagged text.
    :param tagged_words: Tuples of the form (word, pos)
    :param lower: Whether to convert each word to lowercase before lemmatizing.
    :return: A list of lemmas for the input text.
    """
    lemmatizer = WordNetLemmatizer()

    # Convert POS tags to wordnet.
    # TODO: Make this a more general solution to handle different POS taggers
    tags = {
        "NN": wordnet.NOUN,
        "JJ": wordnet.ADJ,
        "VV": wordnet.VERB,
        "RB": wordnet.ADV
    }
    # TODO: Fix the default handling for pos tags.
    return [lemmatizer.lemmatize(word.lower() if lower else word,
                                 pos=tags.get(tag, wordnet.NOUN))
            for word, tag in tagged_words]
