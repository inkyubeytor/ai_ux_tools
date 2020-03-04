from dataset.blogger.blogger import BloggerDataset
from dataset.meetings.meetings import AMIDataset

datasets = {
    "blogs": BloggerDataset,
    "meetings": AMIDataset
}
