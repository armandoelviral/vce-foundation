from epics.epic080_governance_drift_detection.approved_model_manifest import (
    ApprovedModelManifest,
)
from epics.epic080_governance_drift_detection.runtime_model_fingerprint import (
    RuntimeModelFingerprint,
)
from epics.epic080_governance_drift_detection.weight_hash_verifier import (
    verify_weight_hash,
)


def build_manifest(weights_hash="weights-hash-001"):

    return ApprovedModelManifest(
        model_id="credit-risk-model",
        model_version="1.0.0",
        model_hash="model-hash-001",
        weights_hash=weights_hash,
        runtime_image_hash="runtime-image-hash-001",
        approved_by="governance-board",
        approved_at="2026-06-10T00:00:00Z",
    )


def build_fingerprint(weights_hash="weights-hash-001"):

    return RuntimeModelFingerprint(
        model_id="credit-risk-model",
        model_version="1.0.0",
        model_hash="model-hash-001",
        weights_hash=weights_hash,
        runtime_image_hash="runtime-image-hash-001",
        captured_at="2026-06-10T00:01:00Z",
    )


def test_weight_hash_verification_accepts_matching_hash():

    assert (
        verify_weight_hash(
            build_manifest(),
            build_fingerprint(),
        )
        is True
    )


def test_weight_hash_verification_rejects_mismatch():

    assert (
        verify_weight_hash(
            build_manifest(
                weights_hash="weights-hash-approved"
            ),
            build_fingerprint(
                weights_hash="weights-hash-runtime"
            ),
        )
        is False
    )
