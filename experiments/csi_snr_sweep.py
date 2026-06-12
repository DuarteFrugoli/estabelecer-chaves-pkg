from __future__ import annotations

import argparse

import numpy as np

from experiments.utils import save_run
from plkg.radio.channels.rayleigh import complex_noise_variance_from_snr
from plkg.radio.profiles import get_profile
from plkg.simulation import CsiScenario, run_csi_monte_carlo


def run(
    snr_values_db: list[float],
    *,
    trials: int,
    block_length: int,
    seed: int,
    profile_name: str = "nr_fr1_n78",
    alice_bob_correlation: float | None = None,
    alice_eve_correlation: float | None = None,
) -> list[dict[str, float]]:
    profile = get_profile(profile_name)
    if profile.measurement != "csi":
        raise ValueError(f"profile {profile_name!r} is not a CSI profile")
    bob_correlation = (
        profile.alice_bob_correlation
        if alice_bob_correlation is None
        else alice_bob_correlation
    )
    eve_correlation = (
        profile.alice_eve_correlation
        if alice_eve_correlation is None
        else alice_eve_correlation
    )
    rows = []
    for index, snr_db in enumerate(snr_values_db):
        scenario = CsiScenario(
            noise_variance=complex_noise_variance_from_snr(snr_db),
            alice_bob_correlation=bob_correlation,
            alice_eve_correlation=eve_correlation,
            relative_estimation_error=profile.estimation_error,
            sample_interval_s=profile.sample_interval_s,
        )
        result = run_csi_monte_carlo(
            scenario,
            block_length=block_length,
            trials=trials,
            seed=seed + index,
        )
        rows.append({"snr_db": snr_db, **result.as_dict()})

    save_run(
        "csi_snr_sweep",
        {
            "snr_values_db": snr_values_db,
            "trials": trials,
            "block_length": block_length,
            "profile_name": profile_name,
            "alice_bob_correlation": bob_correlation,
            "alice_eve_correlation": eve_correlation,
        },
        rows,
        seed,
    )
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1_000)
    parser.add_argument("--block-length", type=int, default=127)
    parser.add_argument("--seed", type=int, default=20260612)
    parser.add_argument("--profile", default="nr_fr1_n78")
    args = parser.parse_args()
    run(
        np.linspace(-10, 30, 17).tolist(),
        trials=args.trials,
        block_length=args.block_length,
        seed=args.seed,
        profile_name=args.profile,
    )
