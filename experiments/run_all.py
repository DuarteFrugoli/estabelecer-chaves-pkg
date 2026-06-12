from __future__ import annotations

import argparse

from experiments.bch_comparison import run as run_bch
from experiments.csi_snr_sweep import run as run_csi_snr
from experiments.eve_correlation_sweep import run as run_eve
from experiments.guard_band_sweep import run as run_guard_band
from experiments.rssi_noise_sweep import run as run_rssi_noise


def run_all(*, quick: bool, seed: int) -> None:
    trials = 20 if quick else 1_000
    total_observations = 1_000 if quick else 127_000
    failures: list[str] = []
    jobs = [
        (
            "csi_snr_sweep",
            lambda: run_csi_snr(
                [-5.0, 5.0, 15.0] if quick else list(range(-10, 31, 5)),
                trials=trials,
                block_length=127,
                seed=seed,
            ),
        ),
        (
            "rssi_noise_sweep",
            lambda: run_rssi_noise(
                [0.5, 1.5, 3.0],
                trials=trials,
                block_length=127,
                seed=seed + 1_000,
            ),
        ),
        (
            "eve_correlation_sweep",
            lambda: run_eve(
                [-1.0, 0.0, 1.0] if quick else [-1, -0.9, -0.5, 0, 0.5, 0.9, 1],
                trials=trials,
                block_length=127,
                seed=seed + 2_000,
            ),
        ),
        (
            "guard_band_sweep",
            lambda: run_guard_band(
                [0.0, 0.3, 0.7],
                trials=trials,
                block_length=127,
                seed=seed + 3_000,
            ),
        ),
        (
            "bch_comparison",
            lambda: run_bch(
                [7, 15, 127] if quick else [7, 15, 127, 255],
                total_observations=total_observations,
                seed=seed + 4_000,
            ),
        ),
    ]

    for name, job in jobs:
        try:
            job()
            print(f"[OK] {name}")
        except Exception as error:
            failures.append(f"{name}: {error}")
            print(f"[FAIL] {name}: {error}")

    if failures:
        raise SystemExit("Experiment failures:\n" + "\n".join(failures))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--seed", type=int, default=20260612)
    arguments = parser.parse_args()
    run_all(quick=not arguments.full, seed=arguments.seed)
