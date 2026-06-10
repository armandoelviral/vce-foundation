from epics.epic080_governance_drift_detection.approved_model_manifest import (
    ApprovedModelManifest,
)
from epics.epic080_governance_drift_detection.governance_whitelist import (
    GovernanceWhitelist,
)
from epics.epic080_governance_drift_detection.runtime_model_fingerprint import (
    RuntimeModelFingerprint,
)


def build_manifest(
    model_id="credit-risk-model",
    model_version="1.0.0",
    model_hash="model-hash-001",
    weights_hash="weights-hash-001",
    runtime_image_hash="runtime-image-hash-001",
):

    return ApprovedModelManifest(
        model_id=model_id,
        model_version=model_version,
        model_hash=model_hash,
        weights_hash=weights_hash,
        runtime_image_hash=runtime_image_hash,
        approved_by="governance-board",
        approved_at="2026-06-10T00:00:00Z",
    )


def build_fingerprint(
    model_id="credit-risk-model",
    model_version="1.0.0",
    model_hash="model-hash-001",
    weights_hash="weights-hash-001",
    runtime_image_hash="runtime-image-hash-001",
):

    return RuntimeModelFingerprint(
        model_id=model_id,
        model_version=model_version,
        model_hash=model_hash,
        weights_hash=weights_hash,
        runtime_image_hash=runtime_image_hash,
        captured_at="2026-06-10T00:01:00Z",
    )


def test_whitelist_accepts_approved_fingerprint():

    whitelist = GovernanceWhitelist(
        manifests=[
            build_manifest(),
        ]
    )

    assert (
        whitelist.is_approved(
            build_fingerprint()
        )
        is True
    )


def test_whitelist_rejects_unapproved_weight_hash():

    whitelist = GovernanceWhitelist(
        manifests=[
            build_manifest(),
        ]
    )

    assert (
        whitelist.is_approved(
            build_fingerprint(
                weights_hash="tampered-weights"
            )
        )
        is False
    )


def test_whitelist_rejects_unapproved_runtime_image():

    whitelist = GovernanceWhitelist(
        manifests=[
            build_manifest(),
        ]
    )

    assert (
        whitelist.is_approved(
            build_fingerprint(
                runtime_image_hash="tampered-runtime"
            )
        )
        is False
    )


def test_whitelist_supports_multiple_approved_manifests():

    whitelist = GovernanceWhitelist(
        manifests=[
            build_manifest(
                model_version="1.0.0"
            ),
            build_manifest(
                model_version="2.0.0",
                model_hash="model-hash-002",
                weights_hash="weights-hash-002",
                runtime_image_hash="runtime-image-hash-002",
            ),
        ]
    )

    assert (
        whitelist.is_approved(
            build_fingerprint(
                model_version="2.0.0",
                model_hash="model-hash-002",
                weights_hash="weights-hash-002",
                runtime_image_hash="runtime-image-hash-002",
            )
        )
        is True
    )
