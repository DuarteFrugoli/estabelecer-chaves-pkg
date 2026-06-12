import numpy as np

from plkg.core.models import FeatureSeries
from plkg.protocol.quantization import MedianGuardBandQuantizer


def test_observers_use_reference_threshold_and_indices() -> None:
    alice = FeatureSeries(np.array([1.0, 2.0, 3.0, 4.0]), "test")
    bob = FeatureSeries(np.array([1.1, 1.9, 3.1, 3.9]), "test")
    quantizer = MedianGuardBandQuantizer(0.0)

    prepared = quantizer.prepare(alice)
    bob_bits = quantizer.apply(bob, prepared.metadata)

    np.testing.assert_array_equal(prepared.bits, [0, 0, 1, 1])
    np.testing.assert_array_equal(bob_bits, prepared.bits)


def test_guard_band_reduces_retention() -> None:
    features = FeatureSeries(np.linspace(0.0, 1.0, 101), "test")
    without_guard = MedianGuardBandQuantizer(0.0).prepare(features)
    with_guard = MedianGuardBandQuantizer(0.5).prepare(features)

    assert with_guard.retention_rate < without_guard.retention_rate
