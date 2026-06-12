from epics.epic085_policy_authority_layer.policy_approval_workflow import (
    PolicyApproval,
)
from epics.epic085_policy_authority_layer.policy_attestation import (
    create_policy_attestation,
)
from epics.epic085_policy_authority_layer.policy_registry import (
    GovernancePolicy,
)


def build_policy():

    return GovernancePolicy(
        policy_id="clinical-admission-policy",
        policy_version="1.0.0",
        policy_hash="policy-hash-001",
        active=True,
    )


def build_approval(
    status="APPROVED",
):

    return PolicyApproval(
        policy_id="clinical-admission-policy",
        policy_version="1.0.0",
        approved_by="governance-board",
        approved_at="2026-06-10T00:00:00Z",
        approval_status=status,
    )


def test_policy_attestation_creation():

    attestation = create_policy_attestation(
        build_policy(),
        build_approval(),
    )

    assert attestation.policy_id == "clinical-admission-policy"
    assert attestation.policy_version == "1.0.0"
    assert attestation.approval_status == "APPROVED"


def test_policy_attestation_contains_signature():

    attestation = create_policy_attestation(
        build_policy(),
        build_approval(),
    )

    assert len(attestation.signature) == 64


def test_policy_attestation_serializes():

    attestation = create_policy_attestation(
        build_policy(),
        build_approval(),
    )

    payload = attestation.to_dict()

    assert payload["policy_id"] == "clinical-admission-policy"
    assert payload["policy_hash"] == "policy-hash-001"
    assert payload["signature"] == attestation.signature


def test_policy_attestation_records_rejected_policy():

    attestation = create_policy_attestation(
        build_policy(),
        build_approval(
            status="REJECTED"
        ),
    )

    assert attestation.approval_status == "REJECTED"
    assert len(attestation.signature) == 64
