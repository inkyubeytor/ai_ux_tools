import argparse
from summarizer import summarizer
from dataset import dataset


def summarize(dataset_type: str, dataset_dir: str,
              summarizer_type: str, output_dir: str) -> None:
    """
    Summarize a dataset with the given method.
    :param dataset_type: The type of dataset to use.
    :param dataset_dir: The root of the dataset directory to summarize.
    :param summarizer_type: The summarization mode to use.
    :param output_dir: The directory to store the summaries.
    :return: None
    """
    dataset_class = dataset.datasets.get(dataset_type)
    summarizer_class = summarizer.summarizers.get(summarizer_type)
    summary_tool = summarizer_class(dataset_class(dataset_dir))
    summary_tool.summarize_dataset(output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="summarize an input text")
    parser.add_argument("dataset_type", type=str,
                        help="type of dataset to use",
                        choices=list(dataset.datasets.keys()))
    parser.add_argument("dataset_dir", type=str,
                        help="path to dataset root")
    parser.add_argument("summarizer_type", type=str,
                        help="type of summarizer to use",
                        choices=list(summarizer.summarizers.keys()))
    parser.add_argument("output_dir", type=str,
                        help="path to output directory")
    args = vars(parser.parse_args())
    summarize(
        args.get("dataset_type"),
        args.get("dataset_dir"),
        args.get("summarizer_type"),
        args.get("output_dir")
    )
