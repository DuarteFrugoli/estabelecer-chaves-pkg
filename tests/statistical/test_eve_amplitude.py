import pytest

from plkg.simulation import CsiScenario, run_csi_monte_carlo


@pytest.mark.statistical
def test_negative_unit_channel_correlation_is_not_secure_for_amplitude() -> None:
    result = run_csi_monte_carlo(
        CsiScenario(
            noise_variance=0.0,
            alice_bob_correlation=1.0,
            alice_eve_correlation=-1.0,
        ),
        block_length=15,
        trials=100,
        seed=9001,
    )

    assert result.eve_raw_mismatch_rate == 0.0
    assert result.mean_alice_eve_correlation == pytest.approx(1.0)
