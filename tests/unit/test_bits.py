import numpy as np
import pytest

from plkg.core.bits import hamming_distance, mismatch_rate, xor_bits


def test_binary_operations() -> None:
    left = np.array([0, 1, 1, 0], dtype=np.uint8)
    right = np.array([1, 1, 0, 0], dtype=np.uint8)

    np.testing.assert_array_equal(xor_bits(left, right), [1, 0, 1, 0])
    assert hamming_distance(left, right) == 2
    assert mismatch_rate(left, right) == 0.5


def test_binary_operations_reject_different_lengths() -> None:
    with pytest.raises(ValueError):
        xor_bits(np.array([0], dtype=np.uint8), np.array([0, 1], dtype=np.uint8))
