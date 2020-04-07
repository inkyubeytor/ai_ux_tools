from dataset.blogger.blogger import BloggerDataset
from dataset.meetings.meetings import AMIDataset
from dataset.test_drive.test_drive import TestDriveDataset
from dataset.test_drive_clean.test_drive_clean import TestDriveCleanDataset

datasets = {
    "blogs": BloggerDataset,
    "meetings": AMIDataset,
    "test_drive": TestDriveDataset,
    "test_drive_clean": TestDriveCleanDataset
}
