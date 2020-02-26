"""
The JTools library for safe interaction with json files.
Written by Abhishek Vijayakumar.
"""
import json
from typing import Dict
import os


def read_file(fp: str) -> [Dict, None]:
    """
    Safe wrapper for `json.load`.
    :param fp: file path
    :return: File data if JSON file, else None.
    """
    try:
        with open(fp, "r") as f:
            return json.load(f)
    except OSError:
        print("OSError: file not found?")
        return None


def write_to_file(fp: str, data: Dict) -> None:
    """
    Safe wrapper for `json.dump`.
    :param fp: The file path to write to
    :param data: The data to save
    :return: None.
    """
    directory = os.path.dirname(fp)
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        with open(fp, "w+") as f:
            json.dump(data, f)
    except OSError:
        print("OSError: file not found?")
    except TypeError:
        print("TypeError: data is not JSON serializable?")


def set_in_file(fp: str, key: str, value, warn: bool = False) -> None:
    """
    Overwrites key-value pair with given pair in file.
    :param fp: The file path to write to
    :param key: The key to write to in the file
    :param value: The value to write into the file
    :param warn: Whether to warn when overwriting data. Defaults to False
    :return: None.
    """
    data = read_file(fp)
    if data is None:
        write_to_file(fp, {key: value})
    else:
        existing = data.get(key)
        if warn and existing is not None:
            print(f"Warning: overwriting {existing}")
        data[key] = value
        write_to_file(fp, data)
