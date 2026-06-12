from __future__ import annotations

import numpy as np
from scipy.special import j0

SPEED_OF_LIGHT_M_S = 299_792_458.0


def doppler_frequency_hz(speed_kmh: float, carrier_frequency_hz: float) -> float:
    if speed_kmh < 0:
        raise ValueError("speed_kmh cannot be negative")
    if carrier_frequency_hz <= 0:
        raise ValueError("carrier_frequency_hz must be positive")
    return (speed_kmh / 3.6) * carrier_frequency_hz / SPEED_OF_LIGHT_M_S


def coherence_time_s(speed_kmh: float, carrier_frequency_hz: float) -> float:
    doppler = doppler_frequency_hz(speed_kmh, carrier_frequency_hz)
    if doppler == 0:
        return float("inf")
    return float(9.0 / (16.0 * np.pi * doppler))


def jakes_correlation(delay_s: float, doppler_hz: float) -> float:
    if delay_s < 0:
        raise ValueError("delay_s cannot be negative")
    if doppler_hz < 0:
        raise ValueError("doppler_hz cannot be negative")
    return float(j0(2.0 * np.pi * doppler_hz * delay_s))
