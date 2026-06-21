from phase4.real_zkvm_integration.proof_artifact_record import (
    ProofArtifactRecord,
)

from phase4.real_zkvm_integration.d5_zk_proof_attachment import (
    D5zkProofAttachment,
)


def test_attachment_contains_d5_artifact_id():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="VERIFIED",
    )

    attachment = D5zkProofAttachment.attach(
        d5_artifact_id="d5-001",
        proof_artifact=artifact,
    )

    assert attachment.d5_artifact_id == "d5-001"


def test_attachment_contains_proof_artifact_id():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="VERIFIED",
    )

    attachment = D5zkProofAttachment.attach(
        d5_artifact_id="d5-001",
        proof_artifact=artifact,
    )

    assert attachment.proof_artifact_id == "artifact-001"


def test_attachment_contains_proof_hash():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="VERIFIED",
    )

    attachment = D5zkProofAttachment.attach(
        d5_artifact_id="d5-001",
        proof_artifact=artifact,
    )

    assert attachment.proof_hash == "proof-001"


def test_attachment_serializes():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="VERIFIED",
    )

    attachment = D5zkProofAttachment.attach(
        d5_artifact_id="d5-001",
        proof_artifact=artifact,
    )

    assert attachment.to_dict() == {
        "d5_artifact_id": "d5-001",
        "proof_artifact_id": "artifact-001",
        "proof_hash": "proof-001",
    }
