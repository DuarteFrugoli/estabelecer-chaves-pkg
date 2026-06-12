from __future__ import annotations

import argparse

from experiments.utils import save_run
from plkg.radio.profiles import get_profile
from plkg.simulation import CsiScenario, run_csi_monte_carlo


def run(
    correlations: list[float],
    *,
    trials: int,
    block_length: int,
    seed: int,
    profile_name: str = "nr_fr1_n78",
) -> list[dict[str, float]]:
    profile = get_profile(profile_name)
    if profile.measurement != "csi":
        raise ValueError(f"profile {profile_name!r} is not a CSI profile")
    rows = []
    for index, correlation in enumerate(correlations):
        scenario = CsiScenario(
            noise_variance=0.02,
            alice_bob_correlation=profile.alice_bob_correlation,
            alice_eve_correlation=correlation,
            relative_estimation_error=profile.estimation_error,
            sample_interval_s=profile.sample_interval_s,
        )
        result = run_csi_monte_carlo(
            scenario,
            block_length=block_length,
            trials=trials,
            seed=seed + index,
        )
        rows.append({"alice_eve_channel_correlation": correlation, **result.as_dict()})

    save_run(
        "eve_correlation_sweep",
        {
            "correlations": correlations,
            "trials": trials,
            "block_length": block_length,
            "profile_name": profile_name,
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
        [-1.0, -0.9, -0.5, 0.0, 0.5, 0.9, 1.0],
        trials=args.trials,
        block_length=args.block_length,
        seed=args.seed,
        profile_name=args.profile,
    )
