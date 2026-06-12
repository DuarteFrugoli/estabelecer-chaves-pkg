from __future__ import annotations

from collections.abc import Callable

import numpy as np

from plkg.core.models import (
    ComplexArray,
    FeatureSeries,
    MonteCarloResult,
    TrialResult,
)
from plkg.protocol.pipeline import execute_protocol
from plkg.protocol.quantization import MedianGuardBandQuantizer
from plkg.protocol.reconciliation import (
    BchCodeOffsetReconciler,
    create_bch_codec,
)
from plkg.radio.channels.rayleigh import (
    correlated_complex_channel,
    sample_rayleigh_channel,
)
from plkg.radio.measurements.csi import CsiAmplitudeExtractor, observe_csi
from plkg.radio.measurements.rssi import RssiLevelExtractor, observe_rssi
from plkg.security.metrics import aggregate_trials
from plkg.simulation.scenario import CsiScenario, RssiScenario

FeatureFactory = Callable[
    [ComplexArray, ComplexArray, ComplexArray, np.random.Generator],
    tuple[FeatureSeries, FeatureSeries, FeatureSeries],
]


def _run_trial(
    sigma: float,
    alice_bob_correlation: float,
    alice_eve_correlation: float,
    guard_band_sigma: float,
    block_length: int,
    rng: np.random.Generator,
    feature_factory: FeatureFactory,
) -> TrialResult:
    quantizer = MedianGuardBandQuantizer(guard_band_sigma)
    reconciler = BchCodeOffsetReconciler(create_bch_codec(block_length))
    sample_count = block_length * (3 if guard_band_sigma > 0 else 1)

    for _ in range(8):
        alice_channel = sample_rayleigh_channel(sigma, sample_count, rng)
        bob_channel = correlated_complex_channel(
            alice_channel,
            sigma,
            alice_bob_correlation,
            rng,
        )
        eve_channel = correlated_complex_channel(
            alice_channel,
            sigma,
            alice_eve_correlation,
            rng,
        )
        features = feature_factory(alice_channel, bob_channel, eve_channel, rng)
        try:
            return execute_protocol(
                *features,
                quantizer=quantizer,
                reconciler=reconciler,
                rng=rng,
            )
        except RuntimeError:
            sample_count *= 2

    raise RuntimeError("guard band retained too few samples after eight attempts")


def run_csi_trial(
    scenario: CsiScenario,
    block_length: int,
    rng: np.random.Generator,
) -> TrialResult:
    extractor = CsiAmplitudeExtractor()

    def create_features(
        alice_channel: ComplexArray,
        bob_channel: ComplexArray,
        eve_channel: ComplexArray,
        local_rng: np.random.Generator,
    ) -> tuple[FeatureSeries, FeatureSeries, FeatureSeries]:
        observations = [
            observe_csi(
                channel,
                scenario.noise_variance,
                scenario.relative_estimation_error,
                local_rng,
                sample_interval_s=scenario.sample_interval_s,
            )
            for channel in (alice_channel, bob_channel, eve_channel)
        ]
        return tuple(extractor.extract(item) for item in observations)  # type: ignore[return-value]

    return _run_trial(
        scenario.sigma,
        scenario.alice_bob_correlation,
        scenario.alice_eve_correlation,
        scenario.guard_band_sigma,
        block_length,
        rng,
        create_features,
    )


def run_rssi_trial(
    scenario: RssiScenario,
    block_length: int,
    rng: np.random.Generator,
) -> TrialResult:
    extractor = RssiLevelExtractor()

    def create_features(
        alice_channel: ComplexArray,
        bob_channel: ComplexArray,
        eve_channel: ComplexArray,
        local_rng: np.random.Generator,
    ) -> tuple[FeatureSeries, FeatureSeries, FeatureSeries]:
        observations = [
            observe_rssi(
                channel,
                scenario.reference_power_dbm,
                scenario.measurement_noise_std_db,
                scenario.resolution_db,
                local_rng,
                sample_interval_s=scenario.sample_interval_s,
            )
            for channel in (alice_channel, bob_channel, eve_channel)
        ]
        return tuple(extractor.extract(item) for item in observations)  # type: ignore[return-value]

    return _run_trial(
        scenario.sigma,
        scenario.alice_bob_correlation,
        scenario.alice_eve_correlation,
        scenario.guard_band_sigma,
        block_length,
        rng,
        create_features,
    )


def run_csi_monte_carlo(
    scenario: CsiScenario,
    *,
    block_length: int = 127,
    trials: int = 1_000,
    seed: int = 0,
) -> MonteCarloResult:
    if trials <= 0:
        raise ValueError("trials must be positive")
    rng = np.random.default_rng(seed)
    results = [run_csi_trial(scenario, block_length, rng) for _ in range(trials)]
    return aggregate_trials(results, seed)


def run_rssi_monte_carlo(
    scenario: RssiScenario,
    *,
    block_length: int = 127,
    trials: int = 1_000,
    seed: int = 0,
) -> MonteCarloResult:
    if trials <= 0:
        raise ValueError("trials must be positive")
    rng = np.random.default_rng(seed)
    results = [run_rssi_trial(scenario, block_length, rng) for _ in range(trials)]
    return aggregate_trials(results, seed)
