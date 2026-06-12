import numpy as np

from plkg.protocol.reconciliation import (
    BchCodeOffsetReconciler,
    create_bch_codec,
)


def test_bch_corrects_up_to_its_capacity() -> None:
    codec = create_bch_codec(15)
    message = np.array([1, 0, 1, 1, 0, 1, 0], dtype=np.uint8)
    codeword = codec.encode(message)
    corrupted = codeword.copy()
    corrupted[[0, 7]] ^= 1

    corrected, errors = codec.decode_codeword(corrupted)

    np.testing.assert_array_equal(corrected, codeword)
    assert errors == 2


def test_code_offset_transcript_is_reusable_by_any_observer() -> None:
    rng = np.random.default_rng(10)
    reconciler = BchCodeOffsetReconciler(create_bch_codec(7))
    alice = np.array([1, 0, 1, 1, 0, 1, 0], dtype=np.uint8)
    bob = alice.copy()
    eve = alice.copy()
    bob[2] ^= 1
    eve[5] ^= 1

    transcript = reconciler.create_transcript(alice, rng)
    bob_result = reconciler.reconcile(bob, transcript)
    eve_result = reconciler.reconcile(eve, transcript)

    np.testing.assert_array_equal(bob_result.bits, alice)
    np.testing.assert_array_equal(eve_result.bits, alice)
    assert transcript.leakage_bits == 3
