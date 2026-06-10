from epics.epic080_governance_drift_detection.approved_model_manifest import (
    ApprovedModelManifest,
)
from epics.epic080_governance_drift_detection.governance_whitelist import (
    GovernanceWhitelist,
)
from epics.epic080_governance_drift_detection.runtime_model_fingerprint import (
    RuntimeModelFingerprint,
)
from epics.epic080_governance_drift_detection.signed_governance_attestation import (
    create_governance_attestation,
)
from epics.epic080_governance_drift_detection.transaction_blocking_rule import (
    TransactionBlockingRule,
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


def build_fingerprint(
    weights_hash="weights-hash-001",
):

    return RuntimeModelFingerprint(
        model_id="credit-risk-model",
        model_version="1.0.0",
        model_hash="model-hash-001",
        weights_hash=weights_hash,
        runtime_image_hash="runtime-image-hash-001",
        captured_at="2026-06-10T00:01:00Z",
    )


def build_decision(
    fingerprint,
):

    whitelist = GovernanceWhitelist(
        manifests=[
            build_manifest(),
        ]
    )

    rule = TransactionBlockingRule(
        whitelist
    )

    return rule.decision(
        fingerprint
    )


def test_signed_governance_attestation_allows_approved_fingerprint():

    manifest = build_manifest()
    fingerprint = build_fingerprint()

    attestation = create_governance_attestation(
        manifest,
        fingerprint,
        build_decision(
            fingerprint
        ),
    )

    assert attestation.decision == "ALLOW"
    assert attestation.reason == "APPROVED_GOVERNANCE_BASELINE"
    assert len(attestation.signature) == 64


def test_signed_governance_attestation_blocks_drifted_fingerprint():

    manifest = build_manifest()
    fingerprint = build_fingerprint(
        weights_hash="tampered-weights"
    )

    attestation = create_governance_attestation(
        manifest,
        fingerprint,
        build_decision(
            fingerprint
        ),
    )

    assert attestation.decision == "BLOCK"
    assert attestation.reason == "GOVERNANCE_DRIFT_DETECTED"
    assert len(attestation.signature) == 64


def test_signed_governance_attestation_serializes():

    manifest = build_manifest()
    fingerprint = build_fingerprint()

    attestation = create_governance_attestation(
        manifest,
        fingerprint,
        build_decision(
            fingerprint
        ),
    )

    payload = attestation.to_dict()

    assert "manifest_hash" in payload
    assert "fingerprint_hash" in payload
    assert "decision" in payload
    assert "signature" in payload
