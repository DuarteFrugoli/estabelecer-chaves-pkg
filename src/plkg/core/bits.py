from __future__ import annotations

import numpy as np

from plkg.core.models import BitArray, as_bits


def xor_bits(left: BitArray, right: BitArray) -> BitArray:
    left_bits = as_bits(left, name="left")
    right_bits = as_bits(right, name="right")
    if len(left_bits) != len(right_bits):
        raise ValueError("bit arrays must have equal length")
    return np.bitwise_xor(left_bits, right_bits).astype(np.uint8)


def hamming_distance(left: BitArray, right: BitArray) -> int:
    return int(np.count_nonzero(xor_bits(left, right)))


def mismatch_rate(left: BitArray, right: BitArray) -> float:
    left_bits = as_bits(left, name="left")
    if len(left_bits) == 0:
        return 0.0
    return hamming_distance(left_bits, right) / len(left_bits)
