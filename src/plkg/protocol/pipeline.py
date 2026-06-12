from __future__ import annotations

from dataclasses import replace

import numpy as np

from plkg.core.models import (
    FeatureSeries,
    FinalKeyResult,
    FloatArray,
    PublicTranscript,
    QuantizationMetadata,
    TrialResult,
)
from plkg.core.protocols import PrivacyAmplifier, Quantizer, Reconciler
from plkg.protocol.privacy_amplification import ToeplitzHashAmplifier


def _safe_correlation(left: FloatArray, right: FloatArray) -> float:
    if len(left) < 2 or np.std(left) == 0 or np.std(right) == 0:
        return 0.0
    return float(np.corrcoef(left, right)[0, 1])


def execute_protocol(
    alice_features: FeatureSeries,
    bob_features: FeatureSeries,
    eve_features: FeatureSeries,
    quantizer: Quantizer,
    reconciler: Reconciler,
    rng: np.random.Generator,
) -> TrialResult:
    prepared = quantizer.prepare(alice_features)
    block_length = reconciler.block_length
    if len(prepared.bits) < block_length:
        raise RuntimeError("not enough retained samples for one reconciliation block")

    accepted_indices = prepared.metadata.accepted_indices[:block_length]
    metadata = QuantizationMetadata(
        threshold=prepared.metadata.threshold,
        accepted_indices=accepted_indices,
        source_length=prepared.metadata.source_length,
        guard_band_width=prepared.metadata.guard_band_width,
    )
    alice_bits = prepared.bits[:block_length]
    bob_bits = quantizer.apply(bob_features, metadata)
    eve_bits = quantizer.apply(eve_features, metadata)

    reconciliation = reconciler.create_transcript(alice_bits, rng)
    transcript = PublicTranscript(
        quantization=metadata,
        reconciliation=reconciliation,
    )
    bob_reconciled = reconciler.reconcile(bob_bits, reconciliation)
    eve_reconciled = reconciler.reconcile(eve_bits, reconciliation)

    return TrialResult(
        alice_bits=alice_bits,
        bob_bits=bob_bits,
        eve_bits=eve_bits,
        bob_reconciled=bob_reconciled,
        eve_reconciled=eve_reconciled,
        transcript=transcript,
        retention_rate=prepared.retention_rate,
        alice_bob_observation_correlation=_safe_correlation(
            alice_features.values,
            bob_features.values,
        ),
        alice_eve_observation_correlation=_safe_correlation(
            alice_features.values,
            eve_features.values,
        ),
    )


def amplify_reconciled_keys(
    trial: TrialResult,
    output_bits: int,
    rng: np.random.Generator,
    amplifier: PrivacyAmplifier | None = None,
) -> FinalKeyResult:
    """Apply one public universal-hash seed to Alice, Bob and Eve."""
    selected_amplifier = amplifier or ToeplitzHashAmplifier()
    seed = selected_amplifier.generate_seed(
        len(trial.alice_bits),
        output_bits,
        rng,
    )
    transcript = replace(trial.transcript, privacy_seed=seed)
    return FinalKeyResult(
        alice_key=selected_amplifier.extract(
            trial.alice_bits,
            output_bits,
            seed,
        ),
        bob_key=selected_amplifier.extract(
            trial.bob_reconciled.bits,
            output_bits,
            seed,
        ),
        eve_key=selected_amplifier.extract(
            trial.eve_reconciled.bits,
            output_bits,
            seed,
        ),
        transcript=transcript,
    )
