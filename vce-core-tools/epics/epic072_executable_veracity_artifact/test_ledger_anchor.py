from epics.epic072_executable_veracity_artifact.ledger_anchor import (
    anchor_artifact,
)

from epics.epic072_executable_veracity_artifact.veracity_artifact import (
    VeracityArtifact,
)


def build_artifact():

    return VeracityArtifact(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "abc"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "xyz"},
        governance={"schema_version": "1.0"},
    )


def test_anchor_returns_receipt():

    artifact = build_artifact()

    receipt = anchor_artifact(
        artifact
    )

    assert receipt.anchoring_status == "ANCHORED"


def test_receipt_contains_artifact_hash():

    artifact = build_artifact()

    receipt = anchor_artifact(
        artifact
    )

    assert (
        receipt.artifact_hash
        ==
        artifact.compute_hash()
    )


def test_receipt_contains_sequence_number():

    artifact = build_artifact()

    receipt = anchor_artifact(
        artifact,
        ledger_sequence=42,
    )

    assert receipt.ledger_sequence == 42
