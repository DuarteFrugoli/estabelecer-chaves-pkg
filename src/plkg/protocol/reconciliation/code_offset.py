from __future__ import annotations

import numpy as np

from plkg.core.bits import xor_bits
from plkg.core.models import (
    BitArray,
    ReconciliationResult,
    ReconciliationTranscript,
    as_bits,
)
from plkg.protocol.reconciliation.bch import BchCodec


class BchCodeOffsetReconciler:
    def __init__(self, codec: BchCodec) -> None:
        self.codec = codec

    @property
    def block_length(self) -> int:
        return self.codec.n

    def create_transcript(
        self,
        reference_bits: BitArray,
        rng: np.random.Generator,
    ) -> ReconciliationTranscript:
        reference = as_bits(reference_bits, name="reference_bits")
        if len(reference) != self.codec.n:
            raise ValueError(f"expected {self.codec.n} reference bits")
        message = rng.integers(0, 2, self.codec.k, dtype=np.uint8)
        codeword = self.codec.encode(message)
        helper_data = xor_bits(reference, codeword)
        return ReconciliationTranscript(
            scheme=f"BCH({self.codec.n},{self.codec.k})-code-offset",
            helper_data=helper_data,
            leakage_bits=self.codec.n - self.codec.k,
        )

    def reconcile(
        self,
        observed_bits: BitArray,
        transcript: ReconciliationTranscript,
    ) -> ReconciliationResult:
        observed = as_bits(observed_bits, name="observed_bits")
        if len(observed) != self.codec.n:
            raise ValueError(f"expected {self.codec.n} observed bits")
        if len(transcript.helper_data) != self.codec.n:
            raise ValueError("transcript does not match the BCH block length")

        noisy_codeword = xor_bits(observed, transcript.helper_data)
        corrected_codeword, corrected_errors = self.codec.decode_codeword(
            noisy_codeword
        )
        reconciled = xor_bits(transcript.helper_data, corrected_codeword)
        return ReconciliationResult(
            bits=reconciled,
            success=corrected_errors is not None,
            corrected_errors=corrected_errors,
        )
