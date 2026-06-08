import json

from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)


def test_sdk_end_to_end_proof_flow():

    runtime = VeracityRuntime()

    proof = runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
        ledger_sequence=21,
    )

    exported = runtime.export_proof(
        proof
    )

    exported_payload = json.loads(
        exported
    )

    audit = runtime.audit_proof(
        proof
    )

    assert proof["verified"] is True
    assert exported_payload["verified"] is True
    assert exported_payload["ledger_sequence"] == 21
    assert audit["audit_status"] == "PASSED"
    assert audit["verified"] is True
