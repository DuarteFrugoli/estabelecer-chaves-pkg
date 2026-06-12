import numpy as np

from plkg.protocol import amplify_reconciled_keys
from plkg.simulation.runner import run_csi_monte_carlo, run_csi_trial
from plkg.simulation.scenario import CsiScenario


def test_identical_csi_without_noise_produces_equal_keys() -> None:
    result = run_csi_monte_carlo(
        CsiScenario(
            noise_variance=0.0,
            alice_bob_correlation=1.0,
            alice_eve_correlation=0.0,
        ),
        block_length=7,
        trials=20,
        seed=123,
    )

    assert result.bob_raw_mismatch_rate == 0.0
    assert result.bob_reconciled_mismatch_rate == 0.0


def test_bob_and_eve_receive_the_same_public_transcript() -> None:
    trial = run_csi_trial(
        CsiScenario(noise_variance=0.02),
        block_length=7,
        rng=np.random.default_rng(3),
    )

    assert len(trial.transcript.reconciliation.helper_data) == 7
    assert trial.transcript.quantization is not None


def test_privacy_amplification_uses_one_public_seed() -> None:
    rng = np.random.default_rng(11)
    trial = run_csi_trial(
        CsiScenario(
            noise_variance=0.0,
            alice_bob_correlation=1.0,
        ),
        block_length=15,
        rng=rng,
    )
    final = amplify_reconciled_keys(trial, output_bits=5, rng=rng)

    np.testing.assert_array_equal(final.alice_key, final.bob_key)
    assert len(final.transcript.privacy_seed) == 19
