from itertools import count

from lib import json_tools as jtools
from preprocessing import xml_parser, cleaning, lemmatization, analysis

FILE = "780903.male.25.Student.Aquarius"

# Clean XML of a blog post.
raw_posts = xml_parser.retrieve_posts(
                xml_parser.load_xml(
                    f"C:/Users/vijay/Documents/nlp-datasets/blogs/{FILE}.xml"))


def e_summarize(post: str, threshold: float = 1.5) -> str:
    """
    Perform extractive text summarization on an input text.
    :param post: A blog post to summarize.
    :param threshold: The relative score threshold for the inclusion of a
    sentence in a summary.
    :return: An extractive text summarization.
    """
    # Convert sentences into lists of words.
    sentences = cleaning.sentences(post)
    sentences = cleaning.remove_punctuation(sentences)
    words = [cleaning.words(s) for s in sentences]
    words = [cleaning.remove_stop_words(s) for s in words]

    # Use POS tagging to lemmatize input.
    lemmas = [lemmatization.lemmatize(lemmatization.pos_tag(s)) for s in words]

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


# TODO: Optimize jtools call?
summary_gen = ({"post": p, "summary": e_summarize(p)} for p in raw_posts)
for g, i in zip(summary_gen, count()):
    jtools.set_in_file(
        f"C:/Users/vijay/Documents/nlp-datasets/blogs_summaries/{FILE}.json",
        i,
        g
    )
