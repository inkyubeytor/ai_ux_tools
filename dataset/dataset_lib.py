# Library for dataset helper functions.
import os


def get_size(start_path):
    """
    Gets the size of a directory recursively.
    From https://gist.github.com/SteveClement/3755572.
    :param start_path: The path to compute size of.
    :return: The size of the directory on disk.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

