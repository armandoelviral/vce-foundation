from epics.epic080_governance_drift_detection.approved_model_manifest import (
    ApprovedModelManifest,
)


def build_manifest():

    return ApprovedModelManifest(
        model_id="credit-risk-model",
        model_version="1.0.0",
        model_hash="model-hash-001",
        weights_hash="weights-hash-001",
        runtime_image_hash="runtime-image-hash-001",
        approved_by="governance-board",
        approved_at="2026-06-10T00:00:00Z",
    )


def test_manifest_creation():

    manifest = build_manifest()

    assert manifest.model_id == "credit-risk-model"
    assert manifest.model_version == "1.0.0"


def test_manifest_contains_hashes():

    manifest = build_manifest()

    assert manifest.model_hash == "model-hash-001"
    assert manifest.weights_hash == "weights-hash-001"
    assert manifest.runtime_image_hash == "runtime-image-hash-001"


def test_manifest_contains_approval_metadata():

    manifest = build_manifest()

    assert manifest.approved_by == "governance-board"
    assert manifest.approved_at == "2026-06-10T00:00:00Z"


def test_manifest_serializes_to_dict():

    manifest = build_manifest()

    payload = manifest.to_dict()

    assert payload["model_id"] == "credit-risk-model"
    assert payload["weights_hash"] == "weights-hash-001"
    assert payload["runtime_image_hash"] == "runtime-image-hash-001"
