from epics.ztc20_confidential_compute_attestation.attestation_evidence import (
    AttestationEvidence,
)

from epics.ztc20_confidential_compute_attestation.attestation_verifier import (
    AttestationVerifier,
)

from epics.ztc20_confidential_compute_attestation.witness_attestation_policy import (
    WitnessAttestationPolicy,
)

from epics.ztc20_confidential_compute_attestation.attestation_admission_record import (
    AttestationAdmissionRecord,
)

from epics.ztc20_confidential_compute_attestation.attested_witness_registry import (
    AttestedWitnessRegistry,
)

from epics.ztc20_confidential_compute_attestation.multicloud_attestation_consensus import (
    MultiCloudAttestationConsensus,
)


def test_end_to_end_confidential_compute_attestation():

    aws_evidence = AttestationEvidence(
        witness_id="witness-aws",
        provider="aws",
        evidence_hash="hash-aws",
    )

    gcp_evidence = AttestationEvidence(
        witness_id="witness-gcp",
        provider="gcp",
        evidence_hash="hash-gcp",
    )

    azure_evidence = AttestationEvidence(
        witness_id="witness-azure",
        provider="azure",
        evidence_hash="hash-azure",
    )

    assert AttestationVerifier.verify(
        aws_evidence
    )

    assert AttestationVerifier.verify(
        gcp_evidence
    )

    assert AttestationVerifier.verify(
        azure_evidence
    )

    policy = WitnessAttestationPolicy()

    aws_admitted = policy.admit(
        verified=True,
    )

    gcp_admitted = policy.admit(
        verified=True,
    )

    azure_admitted = policy.admit(
        verified=True,
    )

    registry = AttestedWitnessRegistry()

    registry.add(
        AttestationAdmissionRecord(
            witness_id="witness-aws",
            admitted=aws_admitted,
            reason="attestation_verified",
        )
    )

    registry.add(
        AttestationAdmissionRecord(
            witness_id="witness-gcp",
            admitted=gcp_admitted,
            reason="attestation_verified",
        )
    )

    registry.add(
        AttestationAdmissionRecord(
            witness_id="witness-azure",
            admitted=azure_admitted,
            reason="attestation_verified",
        )
    )

    assert registry.is_attested(
        "witness-aws"
    )

    assert registry.is_attested(
        "witness-gcp"
    )

    assert registry.is_attested(
        "witness-azure"
    )

    consensus = MultiCloudAttestationConsensus()

    assert consensus.has_consensus(
        total_witnesses=3,
        attested_witnesses=3,
    )
