from typing import Dict, List


def frequency_table(words: List[str]) -> Dict[str, int]:
    """
    Creates a frequency table for words in an input list.
    :param words: The list of words to count (usually lemmatized).
    :return: A frequency table with counts of each word.
    """
    table = {}
    for word in words:
        try:
            table[word] += 1
        except KeyError:
            table[word] = 1
    return table
