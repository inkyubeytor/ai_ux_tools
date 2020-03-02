from typing import List

import lib.json_tools as jtools


def save(raw: List[str], summary: List[str], fp: str) -> None:
    """
    Saves element summary data to json file.
    :param raw: The input data to the summarizer.
    :param summary: The computed summary.
    :param fp: The path to save the data to.
    :return: None
    """
    data = {i: {"input": raw[i], "output": summary[i]}
            for i in range(len(raw))}
    jtools.write_to_file(fp, data)
