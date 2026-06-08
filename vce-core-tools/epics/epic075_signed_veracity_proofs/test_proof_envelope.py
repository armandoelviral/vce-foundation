from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)
from epics.epic075_signed_veracity_proofs.proof_envelope import (
    SignedProofEnvelope,
    build_unsigned_envelope,
)


def build_proof():

    runtime = VeracityRuntime()

    return runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )


def test_builds_unsigned_envelope():

    proof = build_proof()

    envelope = build_unsigned_envelope(
        proof
    )

    assert isinstance(
        envelope,
        SignedProofEnvelope,
    )


def test_envelope_contains_open_vce_payload():

    proof = build_proof()

    envelope = build_unsigned_envelope(
        proof
    )

    assert "identity" in envelope.open_vce_payload
    assert "provenance" in envelope.open_vce_payload
    assert "replay" in envelope.open_vce_payload


def test_envelope_does_not_mutate_original_proof():

    proof = build_proof()

    original_hash = proof["receipt"].artifact_hash

    envelope = build_unsigned_envelope(
        proof
    )

    assert envelope.artifact_hash == original_hash
    assert proof["receipt"].artifact_hash == original_hash
