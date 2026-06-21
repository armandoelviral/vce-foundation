from phase4.real_zkvm_integration.proof_artifact_record import (
    ProofArtifactRecord,
)

from phase4.real_zkvm_integration.proof_artifact_verifier import (
    ProofArtifactVerifier,
)


def test_valid_artifact_verifies():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="UNVERIFIED",
    )

    assert ProofArtifactVerifier.verify(artifact) is True


def test_missing_artifact_id_fails():

    artifact = ProofArtifactRecord(
        artifact_id="",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="UNVERIFIED",
    )

    assert ProofArtifactVerifier.verify(artifact) is False


def test_missing_execution_request_id_fails():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="UNVERIFIED",
    )

    assert ProofArtifactVerifier.verify(artifact) is False


def test_missing_prover_type_fails():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="",
        proof_hash="proof-001",
        verification_status="UNVERIFIED",
    )

    assert ProofArtifactVerifier.verify(artifact) is False


def test_missing_proof_hash_fails():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="",
        verification_status="UNVERIFIED",
    )

    assert ProofArtifactVerifier.verify(artifact) is False
