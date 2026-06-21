from phase4.real_zkvm_integration.proof_artifact_record import (
    ProofArtifactRecord,
)


def test_contains_artifact_id():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="UNVERIFIED",
    )

    assert (
        artifact.artifact_id
        == "artifact-001"
    )


def test_contains_execution_request_id():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="UNVERIFIED",
    )

    assert (
        artifact.execution_request_id
        == "request-001"
    )


def test_contains_prover_type():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="UNVERIFIED",
    )

    assert (
        artifact.prover_type
        == "SP1"
    )


def test_contains_proof_hash():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="UNVERIFIED",
    )

    assert (
        artifact.proof_hash
        == "proof-001"
    )


def test_contains_verification_status():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="UNVERIFIED",
    )

    assert (
        artifact.verification_status
        == "UNVERIFIED"
    )


def test_serializes():

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id="request-001",
        prover_type="SP1",
        proof_hash="proof-001",
        verification_status="UNVERIFIED",
    )

    assert artifact.to_dict() == {
        "artifact_id":
            "artifact-001",

        "execution_request_id":
            "request-001",

        "prover_type":
            "SP1",

        "proof_hash":
            "proof-001",

        "verification_status":
            "UNVERIFIED",
    }
