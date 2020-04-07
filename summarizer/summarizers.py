from summarizer.frequency.frequency import FrequencySummarizer
from summarizer.textrank.textrank import TextRankSummarizer
from summarizer.presumm.presumm import PreSummSummarizer

summarizers = {
    "frequency": FrequencySummarizer,
    "textrank": TextRankSummarizer,
    "presumm": PreSummSummarizer
}
