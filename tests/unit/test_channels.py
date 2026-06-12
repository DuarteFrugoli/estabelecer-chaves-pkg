import numpy as np
import pytest

from plkg.radio.channels.mobility import (
    coherence_time_s,
    doppler_frequency_hz,
    jakes_correlation,
)
from plkg.radio.channels.rayleigh import (
    add_complex_estimation_noise,
    correlated_complex_channel,
    sample_rayleigh_channel,
)


def test_correlated_channel_matches_requested_correlation() -> None:
    rng = np.random.default_rng(42)
    alice = sample_rayleigh_channel(1.0, 100_000, rng)
    bob = correlated_complex_channel(alice, 1.0, 0.75, rng)

    assert np.corrcoef(alice.real, bob.real)[0, 1] == pytest.approx(0.75, abs=0.02)
    assert np.corrcoef(alice.imag, bob.imag)[0, 1] == pytest.approx(0.75, abs=0.02)


def test_estimation_without_noise_preserves_channel() -> None:
    rng = np.random.default_rng(1)
    channel = sample_rayleigh_channel(1.0, 32, rng)
    observed = add_complex_estimation_noise(channel, 0.0, 0.0, rng)
    np.testing.assert_array_equal(observed, channel)


def test_mobility_model() -> None:
    assert doppler_frequency_hz(0.0, 2.4e9) == 0.0
    assert coherence_time_s(0.0, 2.4e9) == float("inf")
    assert jakes_correlation(0.0, 100.0) == pytest.approx(1.0)
