import json

from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)
from epics.epic075_signed_veracity_proofs.proof_envelope import (
    build_unsigned_envelope,
)


def build_envelope():

    runtime = VeracityRuntime()

    proof = runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )

    return build_unsigned_envelope(
        proof
    )


def test_signing_payload_is_deterministic():

    envelope_a = build_envelope()
    envelope_b = build_envelope()

    assert (
        envelope_a.signing_payload()
        ==
        envelope_b.signing_payload()
    )


def test_signing_payload_excludes_signature():

    envelope = build_envelope()

    payload = envelope.signing_payload()

    decoded = json.loads(
        payload
    )

    assert "signature" not in decoded

    assert "rekor_set" not in decoded


def test_signing_payload_contains_artifact_hash():

    envelope = build_envelope()

    payload = envelope.signing_payload()

    assert envelope.artifact_hash in payload
