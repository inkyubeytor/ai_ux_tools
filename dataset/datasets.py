from dataset.blogger.blogger import BloggerDataset
from dataset.meetings.meetings import AMIDataset
from dataset.test_drive.test_drive import TestDriveDataset

datasets = {
    "blogs": BloggerDataset,
    "meetings": AMIDataset,
    "test_drive": TestDriveDataset
}
