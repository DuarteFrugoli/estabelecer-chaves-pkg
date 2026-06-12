from __future__ import annotations

import argparse

from experiments.utils import save_run
from plkg.radio.profiles import get_profile
from plkg.simulation import RssiScenario, run_rssi_monte_carlo


def run(
    noise_values_db: list[float],
    *,
    trials: int,
    block_length: int,
    seed: int,
    profile_name: str = "iot_static_sensor",
) -> list[dict[str, float]]:
    profile = get_profile(profile_name)
    if profile.measurement != "rssi":
        raise ValueError(f"profile {profile_name!r} is not an RSSI profile")
    rows = []
    for index, noise_std_db in enumerate(noise_values_db):
        scenario = RssiScenario(
            reference_power_dbm=profile.rssi_reference_power_dbm,
            measurement_noise_std_db=noise_std_db,
            resolution_db=profile.rssi_resolution_db,
            alice_bob_correlation=profile.alice_bob_correlation,
            alice_eve_correlation=profile.alice_eve_correlation,
            sample_interval_s=profile.sample_interval_s,
        )
        result = run_rssi_monte_carlo(
            scenario,
            block_length=block_length,
            trials=trials,
            seed=seed + index,
        )
        rows.append({"measurement_noise_std_db": noise_std_db, **result.as_dict()})

    save_run(
        "rssi_noise_sweep",
        {
            "noise_values_db": noise_values_db,
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
    parser.add_argument("--profile", default="iot_static_sensor")
    args = parser.parse_args()
    run(
        [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0],
        trials=args.trials,
        block_length=args.block_length,
        seed=args.seed,
        profile_name=args.profile,
    )
