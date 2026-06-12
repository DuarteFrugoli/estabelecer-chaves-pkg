from __future__ import annotations

from dataclasses import dataclass


def _validate_common(
    sigma: float,
    alice_bob_correlation: float,
    alice_eve_correlation: float,
    guard_band_sigma: float,
) -> None:
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    if not -1 <= alice_bob_correlation <= 1:
        raise ValueError("alice_bob_correlation must be in [-1, 1]")
    if not -1 <= alice_eve_correlation <= 1:
        raise ValueError("alice_eve_correlation must be in [-1, 1]")
    if guard_band_sigma < 0:
        raise ValueError("guard_band_sigma cannot be negative")


@dataclass(frozen=True)
class CsiScenario:
    sigma: float = 1 / (2**0.5)
    noise_variance: float = 0.0
    alice_bob_correlation: float = 0.95
    alice_eve_correlation: float = 0.0
    relative_estimation_error: float = 0.0
    guard_band_sigma: float = 0.0
    sample_interval_s: float = 1e-3

    def __post_init__(self) -> None:
        _validate_common(
            self.sigma,
            self.alice_bob_correlation,
            self.alice_eve_correlation,
            self.guard_band_sigma,
        )
        if self.noise_variance < 0:
            raise ValueError("noise_variance cannot be negative")
        if self.relative_estimation_error < 0:
            raise ValueError("relative_estimation_error cannot be negative")


@dataclass(frozen=True)
class RssiScenario:
    sigma: float = 1 / (2**0.5)
    reference_power_dbm: float = -60.0
    measurement_noise_std_db: float = 1.5
    resolution_db: float = 1.0
    alice_bob_correlation: float = 0.95
    alice_eve_correlation: float = 0.0
    guard_band_sigma: float = 0.0
    sample_interval_s: float = 0.1

    def __post_init__(self) -> None:
        _validate_common(
            self.sigma,
            self.alice_bob_correlation,
            self.alice_eve_correlation,
            self.guard_band_sigma,
        )
        if self.measurement_noise_std_db < 0:
            raise ValueError("measurement_noise_std_db cannot be negative")
        if self.resolution_db <= 0:
            raise ValueError("resolution_db must be positive")
