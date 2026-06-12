import numpy as np

from plkg.radio.measurements.csi import CsiAmplitudeExtractor, observe_csi
from plkg.radio.measurements.rssi import RssiLevelExtractor, observe_rssi


def test_csi_and_rssi_are_distinct_observation_types() -> None:
    rng = np.random.default_rng(7)
    channel = np.array([1 + 1j, 0.5 + 0.25j])

    csi = observe_csi(channel, 0.0, 0.0, rng)
    rssi = observe_rssi(channel, -60.0, 0.0, 1.0, rng)

    np.testing.assert_allclose(
        CsiAmplitudeExtractor().extract(csi).values,
        np.abs(channel),
    )
    assert RssiLevelExtractor().extract(rssi).name == "rssi_level"
    assert np.all(np.mod(rssi.values_dbm, 1.0) == 0)
