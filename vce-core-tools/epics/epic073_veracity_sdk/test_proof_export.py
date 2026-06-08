import json

from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)


def test_export_proof_returns_json():

    runtime = VeracityRuntime()

    proof = runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )

    exported = runtime.export_proof(
        proof
    )

    payload = json.loads(
        exported
    )

    assert payload["verified"] is True


def test_export_contains_core_fields():

    runtime = VeracityRuntime()

    proof = runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )

    exported = runtime.export_proof(
        proof
    )

    payload = json.loads(
        exported
    )

    assert "artifact_hash" in payload
    assert "ledger_sequence" in payload
    assert "verified" in payload
