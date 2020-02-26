from typing import List

from bs4 import BeautifulSoup


def load_xml(fp: str) -> BeautifulSoup:
    """
    Loads an xml file and returns its contents.
    :param fp: The path of the file to load.
    :return: A BeautifulSoup object containing the contents of the file.
    """
    return BeautifulSoup(open(fp, "r"), 'lxml')


def retrieve_posts(soup: BeautifulSoup) -> List[str]:
    """
    Returns the blog posts of a soup as separate strings. Intended for use with
    the blogs corpus at http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm.
    :param soup: The input soup (XML or HTML).
    :return: A list with a string for each post.
    """
    return [post.text.strip(" \n\t") for post in soup.find_all("post")]
