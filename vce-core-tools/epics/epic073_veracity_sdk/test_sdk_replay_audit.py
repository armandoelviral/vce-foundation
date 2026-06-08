from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)


def test_sdk_replay_audit_passes_for_valid_proof():

    runtime = VeracityRuntime()

    proof = runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )

    audit = runtime.audit_proof(
        proof
    )

    assert audit["audit_status"] == "PASSED"
    assert audit["verified"] is True


def test_sdk_replay_audit_contains_receipt_fields():

    runtime = VeracityRuntime()

    proof = runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
        ledger_sequence=11,
    )

    audit = runtime.audit_proof(
        proof
    )

    assert "artifact_hash" in audit
    assert audit["ledger_sequence"] == 11
