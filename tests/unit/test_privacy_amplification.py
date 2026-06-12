import numpy as np
import pytest

from plkg.protocol.privacy_amplification import ToeplitzHashAmplifier


def test_toeplitz_hash_is_reproducible_and_has_requested_length() -> None:
    amplifier = ToeplitzHashAmplifier()
    rng = np.random.default_rng(42)
    source = rng.integers(0, 2, 64, dtype=np.uint8)
    seed = amplifier.generate_seed(64, 32, rng)

    first = amplifier.extract(source, 32, seed)
    second = amplifier.extract(source, 32, seed)

    np.testing.assert_array_equal(first, second)
    assert len(first) == 32


def test_toeplitz_hash_does_not_expand_the_source() -> None:
    with pytest.raises(ValueError):
        ToeplitzHashAmplifier().seed_length(16, 17)
