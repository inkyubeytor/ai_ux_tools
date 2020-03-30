# Nikolas Martelaro test drive dataset
from dataset.dataset import Dataset, Document
import os
from typing import List


class TestDriveDataset(Dataset):
    """
    A dataset containing only Nik's test drive.
    """
    def dataset_info(self, fp: str = None) -> str:
        # TODO: make output json formatted.
        """
        Displays information about the test drive file.
        :param fp: The file path to dump information to. If None, information is
        printed to stdout.
        :return: The dataset summary as a string.
        """
        data = "Nik's Test Drive\n"
        size = os.path.getsize(f"{self.root}/2020-03-03_IKEA-DRIVE_CLIP.txt")
        data += f"Size: {size / 1000} kilobytes"
        if fp is not None:
            with open(fp, "w+") as f:
                f.write(data)
        return data

    def list_documents(self) -> List[str]:
        """
        List all the available documents in the dataset.
        :return: A list of document names.
        """
        return os.listdir(self.root)

    def retrieve_document(self, document_name: str) -> Document:
        """
        Load a document from disk.
        :param document_name: The name of the document to load.
        :return: A loaded document.
        """
        with open(f"{self.root}/{document_name}") as f:
            return [line[max(2, line.find(']') + 2):]
                    for line in f.readlines() if len(line) > 1]
