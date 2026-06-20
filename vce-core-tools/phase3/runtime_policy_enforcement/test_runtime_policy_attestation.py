from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)

from phase3.runtime_policy_enforcement.runtime_policy_attestation import (
    RuntimePolicyAttestation,
)


def test_attestation_subject():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    attestation = (
        RuntimePolicyAttestation.attest(
            attestation_id="att-001",
            policy=policy,
        )
    )

    assert (
        attestation.subject
        == "runtime_policy"
    )


def test_attestation_uses_policy_id():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    attestation = (
        RuntimePolicyAttestation.attest(
            attestation_id="att-001",
            policy=policy,
        )
    )

    assert (
        attestation.evidence_hash
        == "policy-001"
    )


def test_attestation_preserves_id():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    attestation = (
        RuntimePolicyAttestation.attest(
            attestation_id="att-001",
            policy=policy,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
