from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)


def test_runtime_facade_creates_artifact():

    runtime = VeracityRuntime()

    artifact = runtime.create_artifact(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )

    assert artifact.identity["identity_id"] == "id-001"


def test_runtime_facade_anchors_artifact():

    runtime = VeracityRuntime()

    artifact = runtime.create_artifact(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )

    receipt = runtime.anchor(
        artifact,
        ledger_sequence=7,
    )

    assert receipt.anchoring_status == "ANCHORED"
    assert receipt.ledger_sequence == 7


def test_runtime_facade_verifies_artifact():

    runtime = VeracityRuntime()

    artifact = runtime.create_artifact(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )

    receipt = runtime.anchor(
        artifact
    )

    assert runtime.verify(
        artifact,
        receipt,
    ) is True
