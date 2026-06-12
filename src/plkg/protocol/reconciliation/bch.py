from __future__ import annotations

from dataclasses import dataclass

import galois
import numpy as np

from plkg.core.models import BitArray, as_bits

BCH_CONFIGURATIONS = {
    7: (4, 1),
    15: (7, 2),
    127: (64, 10),
    255: (139, 15),
}


@dataclass(frozen=True)
class BchCodec:
    code: galois.BCH

    @property
    def n(self) -> int:
        return int(self.code.n)

    @property
    def k(self) -> int:
        return int(self.code.k)

    @property
    def t(self) -> int:
        return int(self.code.t)

    def encode(self, information_bits: BitArray) -> BitArray:
        bits = as_bits(information_bits, name="information_bits")
        if len(bits) != self.k:
            raise ValueError(f"expected {self.k} information bits")
        return np.asarray(self.code.encode(bits), dtype=np.uint8)

    def decode_codeword(self, received_bits: BitArray) -> tuple[BitArray, int | None]:
        received = as_bits(received_bits, name="received_bits")
        if len(received) != self.n:
            raise ValueError(f"expected a codeword with {self.n} bits")
        try:
            message = self.code.decode(received)
            corrected = np.asarray(self.code.encode(message), dtype=np.uint8)
        except (ValueError, ArithmeticError, RuntimeError):
            return received.copy(), None

        corrected_errors = int(np.count_nonzero(corrected != received))
        if corrected_errors > self.t:
            return received.copy(), None
        return corrected, corrected_errors


def create_bch_codec(
    block_length: int,
    information_length: int | None = None,
) -> BchCodec:
    try:
        expected_k, correction_capacity = BCH_CONFIGURATIONS[block_length]
    except KeyError as error:
        supported = ", ".join(str(length) for length in BCH_CONFIGURATIONS)
        raise ValueError(
            f"unsupported BCH block length {block_length}; supported: {supported}"
        ) from error

    if information_length is not None and information_length != expected_k:
        raise ValueError(
            f"BCH({block_length}, {information_length}) is unsupported; "
            f"expected k={expected_k}"
        )

    minimum_distance = 2 * correction_capacity + 1
    return BchCodec(galois.BCH(block_length, expected_k, minimum_distance))
