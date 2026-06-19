from phase3.governance_inclusion_proof.inclusion_proof_record import (
    InclusionProofRecord,
)

from phase3.governance_inclusion_proof.proof_attestation import (
    ProofAttestation,
)


def test_attestation_subject():

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    attestation = ProofAttestation.attest(
        attestation_id="att-001",
        proof=proof,
    )

    assert attestation.subject == "governance_inclusion_proof"


def test_attestation_uses_proof_hash():

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    attestation = ProofAttestation.attest(
        attestation_id="att-001",
        proof=proof,
    )

    assert attestation.evidence_hash == "proof-hash-001"


def test_attestation_preserves_id():

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    attestation = ProofAttestation.attest(
        attestation_id="att-001",
        proof=proof,
    )

    assert attestation.attestation_id == "att-001"
