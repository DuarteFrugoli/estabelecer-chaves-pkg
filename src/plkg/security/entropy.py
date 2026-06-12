import math


def extractable_key_length(
    min_entropy_bits: float,
    public_leakage_bits: int,
    security_bits: int,
) -> int:
    """Leftover-hash bound for statistical distance at most 2^-security_bits."""
    if min_entropy_bits < 0:
        raise ValueError("min_entropy_bits cannot be negative")
    if public_leakage_bits < 0:
        raise ValueError("public_leakage_bits cannot be negative")
    if security_bits <= 0:
        raise ValueError("security_bits must be positive")
    return max(
        0,
        math.floor(min_entropy_bits - public_leakage_bits - 2 * security_bits),
    )
