from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import NDArray

BitArray = NDArray[np.uint8]
FloatArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]


def as_bits(values: Any, *, name: str = "bits") -> BitArray:
    raw = np.asarray(values)
    if raw.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if not np.all(np.isin(raw, (0, 1))):
        raise ValueError(f"{name} must contain only 0 and 1")
    return raw.astype(np.uint8)


@dataclass(frozen=True)
class CsiObservation:
    values: ComplexArray
    sample_interval_s: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        values = np.asarray(self.values, dtype=np.complex128)
        if values.ndim != 1:
            raise ValueError("CSI values must be one-dimensional")
        if self.sample_interval_s <= 0:
            raise ValueError("sample_interval_s must be positive")
        object.__setattr__(self, "values", values)


@dataclass(frozen=True)
class RssiObservation:
    values_dbm: FloatArray
    sample_interval_s: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        values = np.asarray(self.values_dbm, dtype=np.float64)
        if values.ndim != 1:
            raise ValueError("RSSI values must be one-dimensional")
        if self.sample_interval_s <= 0:
            raise ValueError("sample_interval_s must be positive")
        object.__setattr__(self, "values_dbm", values)


@dataclass(frozen=True)
class FeatureSeries:
    values: FloatArray
    name: str

    def __post_init__(self) -> None:
        values = np.asarray(self.values, dtype=np.float64)
        if values.ndim != 1:
            raise ValueError("features must be one-dimensional")
        object.__setattr__(self, "values", values)


@dataclass(frozen=True)
class QuantizationMetadata:
    threshold: float
    accepted_indices: NDArray[np.int64]
    source_length: int
    guard_band_width: float

    def __post_init__(self) -> None:
        indices = np.asarray(self.accepted_indices, dtype=np.int64)
        if indices.ndim != 1:
            raise ValueError("accepted_indices must be one-dimensional")
        if np.any(indices < 0) or np.any(indices >= self.source_length):
            raise ValueError("accepted_indices contains an invalid index")
        object.__setattr__(self, "accepted_indices", indices)


@dataclass(frozen=True)
class QuantizationResult:
    bits: BitArray
    metadata: QuantizationMetadata

    def __post_init__(self) -> None:
        bits = as_bits(self.bits)
        if len(bits) != len(self.metadata.accepted_indices):
            raise ValueError("bits and accepted_indices must have equal length")
        object.__setattr__(self, "bits", bits)

    @property
    def retention_rate(self) -> float:
        if self.metadata.source_length == 0:
            return 0.0
        return len(self.bits) / self.metadata.source_length


@dataclass(frozen=True)
class ReconciliationTranscript:
    scheme: str
    helper_data: BitArray
    leakage_bits: int

    def __post_init__(self) -> None:
        helper_data = as_bits(self.helper_data, name="helper_data")
        if self.leakage_bits < 0:
            raise ValueError("leakage_bits cannot be negative")
        object.__setattr__(self, "helper_data", helper_data)


@dataclass(frozen=True)
class PublicTranscript:
    quantization: QuantizationMetadata
    reconciliation: ReconciliationTranscript
    privacy_seed: BitArray = field(
        default_factory=lambda: np.array([], dtype=np.uint8)
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "privacy_seed",
            as_bits(self.privacy_seed, name="privacy_seed"),
        )

    @property
    def reconciliation_leakage_bits(self) -> int:
        return self.reconciliation.leakage_bits


@dataclass(frozen=True)
class ReconciliationResult:
    bits: BitArray
    success: bool
    corrected_errors: int | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "bits", as_bits(self.bits))


@dataclass(frozen=True)
class TrialResult:
    alice_bits: BitArray
    bob_bits: BitArray
    eve_bits: BitArray
    bob_reconciled: ReconciliationResult
    eve_reconciled: ReconciliationResult
    transcript: PublicTranscript
    retention_rate: float
    alice_bob_observation_correlation: float
    alice_eve_observation_correlation: float


@dataclass(frozen=True)
class FinalKeyResult:
    alice_key: BitArray
    bob_key: BitArray
    eve_key: BitArray
    transcript: PublicTranscript

    def __post_init__(self) -> None:
        alice_key = as_bits(self.alice_key, name="alice_key")
        bob_key = as_bits(self.bob_key, name="bob_key")
        eve_key = as_bits(self.eve_key, name="eve_key")
        if len({len(alice_key), len(bob_key), len(eve_key)}) != 1:
            raise ValueError("all final keys must have equal length")
        object.__setattr__(self, "alice_key", alice_key)
        object.__setattr__(self, "bob_key", bob_key)
        object.__setattr__(self, "eve_key", eve_key)


@dataclass(frozen=True)
class MonteCarloResult:
    trials: int
    bits_per_trial: int
    bob_raw_mismatch_rate: float
    bob_reconciled_mismatch_rate: float
    bob_frame_error_rate: float
    eve_raw_mismatch_rate: float
    eve_reconciled_mismatch_rate: float
    mean_retention_rate: float
    mean_alice_bob_correlation: float
    mean_alice_eve_correlation: float
    seed: int

    def as_dict(self) -> dict[str, int | float]:
        return {
            field_name: getattr(self, field_name)
            for field_name in self.__dataclass_fields__
        }
