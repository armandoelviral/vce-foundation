from epics.epic080_governance_drift_detection.approved_model_manifest import (
    ApprovedModelManifest,
)
from epics.epic080_governance_drift_detection.governance_whitelist import (
    GovernanceWhitelist,
)
from epics.epic080_governance_drift_detection.runtime_model_fingerprint import (
    RuntimeModelFingerprint,
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


def build_rule():

    whitelist = GovernanceWhitelist(
        manifests=[
            build_manifest(),
        ]
    )

    return TransactionBlockingRule(
        whitelist
    )


def test_blocking_rule_allows_approved_fingerprint():

    rule = build_rule()

    assert (
        rule.should_block(
            build_fingerprint()
        )
        is False
    )


def test_blocking_rule_blocks_drifted_fingerprint():

    rule = build_rule()

    assert (
        rule.should_block(
            build_fingerprint(
                weights_hash="tampered-weights"
            )
        )
        is True
    )


def test_blocking_rule_returns_allowed_decision():

    rule = build_rule()

    decision = rule.decision(
        build_fingerprint()
    )

    assert decision["allowed"] is True
    assert (
        decision["reason"]
        == "APPROVED_GOVERNANCE_BASELINE"
    )


def test_blocking_rule_returns_blocked_decision():

    rule = build_rule()

    decision = rule.decision(
        build_fingerprint(
            weights_hash="tampered-weights"
        )
    )

    assert decision["allowed"] is False
    assert (
        decision["reason"]
        == "GOVERNANCE_DRIFT_DETECTED"
    )
