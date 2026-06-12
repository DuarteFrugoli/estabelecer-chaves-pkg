from __future__ import annotations

import argparse

from experiments.utils import save_run
from plkg.radio.profiles import get_profile
from plkg.simulation import CsiScenario, run_csi_monte_carlo


def run(
    block_lengths: list[int],
    *,
    total_observations: int,
    seed: int,
    profile_name: str = "nr_fr1_n78",
) -> list[dict[str, float]]:
    profile = get_profile(profile_name)
    if profile.measurement != "csi":
        raise ValueError(f"profile {profile_name!r} is not a CSI profile")
    rows = []
    scenario = CsiScenario(
        noise_variance=0.05,
        alice_bob_correlation=profile.alice_bob_correlation,
        alice_eve_correlation=profile.alice_eve_correlation,
        relative_estimation_error=profile.estimation_error,
        sample_interval_s=profile.sample_interval_s,
    )
    for index, block_length in enumerate(block_lengths):
        trials = max(1, total_observations // block_length)
        result = run_csi_monte_carlo(
            scenario,
            block_length=block_length,
            trials=trials,
            seed=seed + index,
        )
        rows.append(
            {
                "block_length": block_length,
                "processed_bits": block_length * trials,
                **result.as_dict(),
            }
        )

    save_run(
        "bch_comparison",
        {
            "block_lengths": block_lengths,
            "total_observations": total_observations,
            "profile_name": profile_name,
        },
        rows,
        seed,
    )
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--total-observations", type=int, default=127_000)
    parser.add_argument("--seed", type=int, default=20260612)
    parser.add_argument("--profile", default="nr_fr1_n78")
    args = parser.parse_args()
    run(
        [7, 15, 127, 255],
        total_observations=args.total_observations,
        seed=args.seed,
        profile_name=args.profile,
    )
