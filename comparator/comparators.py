from comparator.jaccard.jaccard import JaccardComparator
from comparator.cosine.cosine import CosineComparator
from comparator.fasttext.fasttext import FastTextComparator

comparators = {
    "jaccard": JaccardComparator,
    "cosine": CosineComparator,
    "fasttext": FastTextComparator
}
