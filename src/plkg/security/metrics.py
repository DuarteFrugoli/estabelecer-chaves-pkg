from __future__ import annotations

import numpy as np

from plkg.core.bits import hamming_distance
from plkg.core.models import MonteCarloResult, TrialResult


def aggregate_trials(trials: list[TrialResult], seed: int) -> MonteCarloResult:
    if not trials:
        raise ValueError("at least one trial is required")
    block_length = len(trials[0].alice_bits)
    if any(len(trial.alice_bits) != block_length for trial in trials):
        raise ValueError("all trials must use the same block length")

    total_bits = block_length * len(trials)
    bob_raw_errors = sum(
        hamming_distance(trial.alice_bits, trial.bob_bits) for trial in trials
    )
    bob_reconciled_errors = sum(
        hamming_distance(trial.alice_bits, trial.bob_reconciled.bits)
        for trial in trials
    )
    eve_raw_errors = sum(
        hamming_distance(trial.alice_bits, trial.eve_bits) for trial in trials
    )
    eve_reconciled_errors = sum(
        hamming_distance(trial.alice_bits, trial.eve_reconciled.bits)
        for trial in trials
    )
    failed_frames = sum(
        not np.array_equal(trial.alice_bits, trial.bob_reconciled.bits)
        for trial in trials
    )

    return MonteCarloResult(
        trials=len(trials),
        bits_per_trial=block_length,
        bob_raw_mismatch_rate=bob_raw_errors / total_bits,
        bob_reconciled_mismatch_rate=bob_reconciled_errors / total_bits,
        bob_frame_error_rate=failed_frames / len(trials),
        eve_raw_mismatch_rate=eve_raw_errors / total_bits,
        eve_reconciled_mismatch_rate=eve_reconciled_errors / total_bits,
        mean_retention_rate=float(
            np.mean([trial.retention_rate for trial in trials])
        ),
        mean_alice_bob_correlation=float(
            np.mean(
                [trial.alice_bob_observation_correlation for trial in trials]
            )
        ),
        mean_alice_eve_correlation=float(
            np.mean(
                [trial.alice_eve_observation_correlation for trial in trials]
            )
        ),
        seed=seed,
    )
