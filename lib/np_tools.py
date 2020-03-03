# Helper functions for numpy operations
import numpy as np


def upper_tri_optima(data: np.ndarray, k: int, maxima: bool = True) \
        -> np.ndarray:
    """
    Returns an array of the k indices of an input upper-triangular matrix
    (excluding the diagonal) that have the highest values.
    :param data: The input matrix (2D array).
    :param k: The number of indices to return.
    :param maxima: Whether to return maxima (True) or minima (False).
    :return: A list of indices in the original matrix with highest values.
    """
    shape = data.shape
    if len(shape) != 2:
        raise ValueError(f"Input is not a matrix (has dimensions {shape})")
    if shape[0] != shape[1]:
        raise ValueError(f"Input is not square (has dimensions {shape})")
    if not maxima:
        data *= -1
    indices = np.argsort(data, axis=None)
    out = []
    for i in indices:
        if len(out) == k:
            break
        index = [i % shape[0], i // shape[0]]
        if index[0] < index[1]:
            out.append(index)
    if len(out) < k:
        raise ValueError(f"Count of k = {k} too large for "
                         f"matrix with dimensions {shape}")
    return np.array(out)
