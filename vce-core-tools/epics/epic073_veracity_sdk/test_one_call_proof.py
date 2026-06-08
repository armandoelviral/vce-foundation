from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)


def test_runtime_prove_returns_artifact_receipt_and_verification():

    runtime = VeracityRuntime()

    proof = runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
        ledger_sequence=9,
    )

    assert "artifact" in proof
    assert "receipt" in proof
    assert "verified" in proof

    assert proof["verified"] is True
    assert proof["receipt"].ledger_sequence == 9


def test_runtime_prove_receipt_matches_artifact_hash():

    runtime = VeracityRuntime()

    proof = runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )

    artifact = proof["artifact"]
    receipt = proof["receipt"]

    assert receipt.artifact_hash == artifact.compute_hash()
