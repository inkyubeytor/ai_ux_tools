# Blog Authorship Corpus - http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm
import os
from typing import List

from bs4 import BeautifulSoup

from dataset.dataset import Dataset, Document


# TODO: Fix Unicode errors when loading documents
class BloggerDataset(Dataset):
    """
    Implements the Dataset class for the blogs dataset.
    """

    # General Methods

    def dataset_info(self, fp: str = None) -> str:
        # TODO: make output json formatted.
        """
        Displays information about the blogs dataset.
        :param fp: The file path to dump information to. If None, information is
        printed to stdout.
        :return: The dataset summary as a string.
        """
        data = "Blogger Dataset\n"
        data += f"Number of files: {len(os.listdir(self.root))}\n"
        data += f"Directory size: {self.get_size(self.root)}\n"
        if fp is not None:
            with open(fp, "w+") as f:
                f.write(data)
        return data

    # Document Methods

    def list_documents(self) -> List[str]:
        """
        List all the available blog pages.
        :return: A list of document names.
        """
        return os.listdir(self.root)

    def retrieve_document(self, document_name: str) -> Document:
        """
        Load a blog page from disk.
        :param document_name: The name of the blog to load.
        :return: A loaded blog, with each post as a separate.
        """
        soup = BeautifulSoup(open(f"{self.root}/{document_name}", "r"), 'lxml')
        return [post.text.strip(" \n\t") for post in soup.find_all("post")]

    # Element Methods
