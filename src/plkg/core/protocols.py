from __future__ import annotations

from typing import Protocol

import numpy as np

from plkg.core.models import (
    BitArray,
    FeatureSeries,
    QuantizationMetadata,
    QuantizationResult,
    ReconciliationResult,
    ReconciliationTranscript,
)


class FeatureExtractor(Protocol):
    def extract(self, observation: object) -> FeatureSeries: ...


class Quantizer(Protocol):
    def prepare(self, features: FeatureSeries) -> QuantizationResult: ...

    def apply(
        self,
        features: FeatureSeries,
        metadata: QuantizationMetadata,
    ) -> BitArray: ...


class Reconciler(Protocol):
    @property
    def block_length(self) -> int: ...

    def create_transcript(
        self,
        reference_bits: BitArray,
        rng: np.random.Generator,
    ) -> ReconciliationTranscript: ...

    def reconcile(
        self,
        observed_bits: BitArray,
        transcript: ReconciliationTranscript,
    ) -> ReconciliationResult: ...


class PrivacyAmplifier(Protocol):
    def seed_length(self, input_bits: int, output_bits: int) -> int: ...

    def generate_seed(
        self,
        input_bits: int,
        output_bits: int,
        rng: np.random.Generator,
    ) -> BitArray: ...

    def extract(
        self,
        bits: BitArray,
        output_bits: int,
        public_seed: BitArray,
    ) -> BitArray: ...
