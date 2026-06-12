from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from plkg.core.models import (
    BitArray,
    FeatureSeries,
    QuantizationMetadata,
    QuantizationResult,
)


class MedianGuardBandQuantizer:
    def __init__(self, guard_band_sigma: float = 0.0) -> None:
        if guard_band_sigma < 0:
            raise ValueError("guard_band_sigma cannot be negative")
        self.guard_band_sigma = guard_band_sigma

    def prepare(self, features: FeatureSeries) -> QuantizationResult:
        values = features.values
        if len(values) == 0:
            metadata = QuantizationMetadata(
                threshold=0.0,
                accepted_indices=np.array([], dtype=np.int64),
                source_length=0,
                guard_band_width=0.0,
            )
            return QuantizationResult(
                bits=np.array([], dtype=np.uint8),
                metadata=metadata,
            )

        threshold = float(np.median(values))
        width = float(self.guard_band_sigma * np.std(values))
        accepted: NDArray[np.int64]
        if self.guard_band_sigma == 0:
            accepted = np.arange(len(values), dtype=np.int64)
        else:
            accepted = np.asarray(
                np.flatnonzero(np.abs(values - threshold) > width),
                dtype=np.int64,
            )
        bits = (values[accepted] > threshold).astype(np.uint8)
        metadata = QuantizationMetadata(
            threshold=threshold,
            accepted_indices=accepted,
            source_length=len(values),
            guard_band_width=width,
        )
        return QuantizationResult(bits=bits, metadata=metadata)

    def apply(
        self,
        features: FeatureSeries,
        metadata: QuantizationMetadata,
    ) -> BitArray:
        if len(features.values) != metadata.source_length:
            raise ValueError("observer features do not match transcript length")
        return (
            features.values[metadata.accepted_indices] > metadata.threshold
        ).astype(np.uint8)
