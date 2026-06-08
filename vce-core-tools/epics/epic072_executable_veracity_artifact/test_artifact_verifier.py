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
        identity={"identity_id": identity_id},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "abc"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "xyz"},
        governance={"schema_version": "1.0"},
    )


def test_verifier_accepts_matching_artifact_and_receipt():

    artifact = build_artifact()

    receipt = anchor_artifact(
        artifact
    )

    assert (
        verify_artifact(
            artifact,
            receipt,
        )
        is True
    )


def test_verifier_rejects_modified_artifact():

    original = build_artifact(
        identity_id="id-001"
    )

    receipt = anchor_artifact(
        original
    )

    modified = build_artifact(
        identity_id="id-002"
    )

    assert (
        verify_artifact(
            modified,
            receipt,
        )
        is False
    )
