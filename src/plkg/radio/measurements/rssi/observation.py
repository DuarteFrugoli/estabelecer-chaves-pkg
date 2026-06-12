from __future__ import annotations

import numpy as np

from plkg.core.models import ComplexArray, RssiObservation


def observe_rssi(
    channel: ComplexArray,
    reference_power_dbm: float,
    measurement_noise_std_db: float,
    resolution_db: float,
    rng: np.random.Generator,
    *,
    sample_interval_s: float = 1.0,
) -> RssiObservation:
    if measurement_noise_std_db < 0:
        raise ValueError("measurement_noise_std_db cannot be negative")
    if resolution_db <= 0:
        raise ValueError("resolution_db must be positive")

    channel = np.asarray(channel, dtype=np.complex128)
    power = np.maximum(np.abs(channel) ** 2, np.finfo(float).tiny)
    values_dbm = reference_power_dbm + 10.0 * np.log10(power)
    if measurement_noise_std_db > 0:
        values_dbm += rng.normal(0.0, measurement_noise_std_db, len(channel))
    values_dbm = np.round(values_dbm / resolution_db) * resolution_db
    return RssiObservation(
        values_dbm=values_dbm,
        sample_interval_s=sample_interval_s,
        metadata={"resolution_db": resolution_db},
    )
