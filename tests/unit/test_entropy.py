from plkg.security.entropy import extractable_key_length


def test_leftover_hash_bound_accounts_for_leakage_and_security_margin() -> None:
    assert extractable_key_length(200, 20, 40) == 100
    assert extractable_key_length(50, 20, 40) == 0
