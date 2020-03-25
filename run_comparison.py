import argparse
from comparator import comparators
from dataset import datasets
from lib.np_tools import upper_tri_optima
from lib import json_tools as jtools
import numpy as np


def compare(dataset_type: str, dataset_dir: str,
            comparator_type: str, output_dir: str,
            document_index: int, num_pairs: int, similar: bool = True) -> None:
    """
    Summarize a dataset with the given method.
    :param dataset_type: The type of dataset to use.
    :param dataset_dir: The root of the dataset directory.
    :param comparator_type: The comparison mode to use.
    :param output_dir: The directory to store the located pairs.
    :param document_index: The index of documents to use for comparison.
    :param num_pairs: The number of pairs to find.
    :param similar: Whether to pick most similar or most different elements.
    :return: None
    """
    dataset_class = datasets.datasets.get(dataset_type)
    comparator_class = comparators.comparators.get(comparator_type)
    compare_tool = comparator_class(dataset_class(dataset_dir))

    data = compare_tool.dataset.kth_elements(document_index)
    jtools.write_to_file(f"{output_dir}/input.json",
                         {i: data[i] for i in range(len(data))})

    scores = compare_tool.compute_matrix(data)
    np.save(f"{output_dir}/scores.npy", scores)

    top_list = upper_tri_optima(scores, num_pairs, not similar)
    for i in range(len(top_list)):
        entry = {
            "element_1": data[top_list[i, 0]],
            "element_2": data[top_list[i, 1]],
            "score": scores[top_list[i, 0], top_list[i, 1]],
        }
        jtools.set_in_file(f"{output_dir}/ranked_elements.json", str(i), entry)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="compare an input text")
    parser.add_argument("dataset_type", type=str,
                        help="type of dataset to use",
                        choices=list(datasets.datasets.keys()))
    parser.add_argument("dataset_dir", type=str,
                        help="path to dataset root")
    parser.add_argument("comparator_type", type=str,
                        help="type of comparator to use",
                        choices=list(comparators.comparators.keys()))
    parser.add_argument("output_dir", type=str,
                        help="path to output directory")
    parser.add_argument("document_index", type=int,
                        help="index of element in each document to compare")
    parser.add_argument("num_pairs", type=int,
                        help="number of top pairs to return")
    parser.add_argument("similar", type=bool, default=True,
                        help="whether to choose most similar elements (true) "
                             "or most different elements (false)")
    args = vars(parser.parse_args())
    compare(
        args.get("dataset_type"),
        args.get("dataset_dir"),
        args.get("comparator_type"),
        args.get("output_dir"),
        args.get("document_index"),
        args.get("num_pairs"),
        args.get("similar")
    )
