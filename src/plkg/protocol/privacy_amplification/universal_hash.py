from __future__ import annotations

import numpy as np

from plkg.core.models import BitArray, as_bits


class ToeplitzHashAmplifier:
    """Two-universal binary hashing with a public Toeplitz seed."""

    def seed_length(self, input_bits: int, output_bits: int) -> int:
        if input_bits <= 0 or output_bits <= 0:
            raise ValueError("input_bits and output_bits must be positive")
        if output_bits > input_bits:
            raise ValueError("output_bits cannot exceed input_bits")
        return input_bits + output_bits - 1

    def generate_seed(
        self,
        input_bits: int,
        output_bits: int,
        rng: np.random.Generator,
    ) -> BitArray:
        length = self.seed_length(input_bits, output_bits)
        return rng.integers(0, 2, length, dtype=np.uint8)

    def extract(
        self,
        bits: BitArray,
        output_bits: int,
        public_seed: BitArray,
    ) -> BitArray:
        source = as_bits(bits)
        expected_seed_length = self.seed_length(len(source), output_bits)
        seed = as_bits(public_seed, name="public_seed")
        if len(seed) != expected_seed_length:
            raise ValueError(
                f"expected {expected_seed_length} public seed bits"
            )

        row_indices = np.arange(output_bits)[:, None]
        column_indices = np.arange(len(source))[None, :]
        matrix_indices = column_indices - row_indices + output_bits - 1
        toeplitz = seed[matrix_indices]
        result: BitArray = np.asarray(
            np.mod(toeplitz @ source, 2),
            dtype=np.uint8,
        )
        return result
