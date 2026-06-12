from plkg.simulation import RssiScenario, run_rssi_monte_carlo


def test_identical_rssi_without_measurement_noise_produces_equal_keys() -> None:
    result = run_rssi_monte_carlo(
        RssiScenario(
            measurement_noise_std_db=0.0,
            alice_bob_correlation=1.0,
            alice_eve_correlation=0.0,
        ),
        block_length=7,
        trials=20,
        seed=123,
    )

    assert result.bob_raw_mismatch_rate == 0.0
    assert result.bob_reconciled_mismatch_rate == 0.0
