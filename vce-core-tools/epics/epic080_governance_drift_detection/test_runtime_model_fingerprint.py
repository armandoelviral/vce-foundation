from epics.epic080_governance_drift_detection.runtime_model_fingerprint import (
    RuntimeModelFingerprint,
)


def build_fingerprint():

    return RuntimeModelFingerprint(
        model_id="credit-risk-model",
        model_version="1.0.0",
        model_hash="model-hash-001",
        weights_hash="weights-hash-001",
        runtime_image_hash="runtime-image-hash-001",
        captured_at="2026-06-10T00:01:00Z",
    )


def test_runtime_fingerprint_creation():

    fingerprint = build_fingerprint()

    assert fingerprint.model_id == "credit-risk-model"
    assert fingerprint.model_version == "1.0.0"


def test_runtime_fingerprint_contains_hashes():

    fingerprint = build_fingerprint()

    assert fingerprint.model_hash == "model-hash-001"
    assert fingerprint.weights_hash == "weights-hash-001"
    assert fingerprint.runtime_image_hash == "runtime-image-hash-001"


def test_runtime_fingerprint_contains_capture_time():

    fingerprint = build_fingerprint()

    assert fingerprint.captured_at == "2026-06-10T00:01:00Z"


def test_runtime_fingerprint_serializes_to_dict():

    fingerprint = build_fingerprint()

    payload = fingerprint.to_dict()

    assert payload["model_id"] == "credit-risk-model"
    assert payload["weights_hash"] == "weights-hash-001"
    assert payload["captured_at"] == "2026-06-10T00:01:00Z"
