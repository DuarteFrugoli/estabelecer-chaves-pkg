from __future__ import annotations

import numpy as np

from plkg.core.models import ComplexArray


def sample_rayleigh_channel(
    sigma: float,
    size: int,
    rng: np.random.Generator,
) -> ComplexArray:
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    if size < 0:
        raise ValueError("size cannot be negative")
    in_phase = rng.normal(0.0, sigma, size)
    quadrature = rng.normal(0.0, sigma, size)
    return np.asarray(in_phase + 1j * quadrature, dtype=np.complex128)


def correlated_complex_channel(
    reference: ComplexArray,
    sigma: float,
    correlation: float,
    rng: np.random.Generator,
) -> ComplexArray:
    if not -1.0 <= correlation <= 1.0:
        raise ValueError("correlation must be in [-1, 1]")
    reference = np.asarray(reference, dtype=np.complex128)
    independent = sample_rayleigh_channel(sigma, len(reference), rng)
    return np.asarray(
        correlation * reference
        + np.sqrt(max(0.0, 1.0 - correlation**2)) * independent,
        dtype=np.complex128,
    )


def add_complex_estimation_noise(
    channel: ComplexArray,
    noise_variance: float,
    relative_error: float,
    rng: np.random.Generator,
) -> ComplexArray:
    if noise_variance < 0:
        raise ValueError("noise_variance cannot be negative")
    if relative_error < 0:
        raise ValueError("relative_error cannot be negative")

    channel = np.asarray(channel, dtype=np.complex128)
    result = channel.copy()

    if noise_variance > 0:
        component_std = np.sqrt(noise_variance / 2.0)
        noise = rng.normal(0.0, component_std, len(channel))
        noise = noise + 1j * rng.normal(0.0, component_std, len(channel))
        result += noise

    if relative_error > 0:
        error_std = relative_error * np.abs(channel)
        error = rng.normal(0.0, error_std, len(channel))
        error = error + 1j * rng.normal(0.0, error_std, len(channel))
        result += error

    return np.asarray(result, dtype=np.complex128)


def complex_noise_variance_from_snr(
    snr_db: float,
    signal_power: float = 1.0,
) -> float:
    if signal_power <= 0:
        raise ValueError("signal_power must be positive")
    return float(signal_power / (10.0 ** (snr_db / 10.0)))
