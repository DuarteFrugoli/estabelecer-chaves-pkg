from __future__ import annotations

import numpy as np

from plkg.core.models import ComplexArray, CsiObservation
from plkg.radio.channels.rayleigh import add_complex_estimation_noise


def observe_csi(
    channel: ComplexArray,
    noise_variance: float,
    relative_error: float,
    rng: np.random.Generator,
    *,
    sample_interval_s: float = 1.0,
) -> CsiObservation:
    values = add_complex_estimation_noise(
        channel,
        noise_variance,
        relative_error,
        rng,
    )
    return CsiObservation(values=values, sample_interval_s=sample_interval_s)
