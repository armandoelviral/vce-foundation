from phase3.governance_policy_enforcement.policy_activation_record import (
    PolicyActivationRecord,
)

from phase3.governance_policy_enforcement.policy_activation_attestation import (
    PolicyActivationAttestation,
)


def test_attestation_subject():

    activation = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    attestation = (
        PolicyActivationAttestation.attest(
            attestation_id="att-001",
            activation=activation,
        )
    )

    assert (
        attestation.subject
        == "policy_activation"
    )


def test_attestation_uses_activation_id():

    activation = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    attestation = (
        PolicyActivationAttestation.attest(
            attestation_id="att-001",
            activation=activation,
        )
    )

    assert (
        attestation.evidence_hash
        == "activation-001"
    )


def test_attestation_preserves_id():

    activation = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    attestation = (
        PolicyActivationAttestation.attest(
            attestation_id="att-001",
            activation=activation,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
