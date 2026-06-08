from epics.epic072_executable_veracity_artifact.artifact_verifier import (
    verify_artifact,
)

from epics.epic072_executable_veracity_artifact.ledger_anchor import (
    anchor_artifact,
)

from epics.epic072_executable_veracity_artifact.veracity_artifact import (
    VeracityArtifact,
)


def build_artifact(identity_id="id-001"):

    return VeracityArtifact(
        identity={
            "identity_id": identity_id,
        },
        trust={
            "certificate_id": "cert-001",
        },
        provenance={
            "input_hash": "input-001",
        },
        replay={
            "sequence_number": 3,
        },
        evidence={
            "evidence_hash": "evidence-001",
        },
        governance={
            "schema_version": "1.0",
        },
    )


def test_end_to_end_proof_passes():

    artifact = build_artifact()

    receipt = anchor_artifact(
        artifact
    )

    assert verify_artifact(
        artifact,
        receipt,
    )


def test_end_to_end_proof_detects_modification():

    original = build_artifact(
        identity_id="id-001"
    )

    receipt = anchor_artifact(
        original
    )

    modified = build_artifact(
        identity_id="id-002"
    )

    assert not verify_artifact(
        modified,
        receipt,
    )
