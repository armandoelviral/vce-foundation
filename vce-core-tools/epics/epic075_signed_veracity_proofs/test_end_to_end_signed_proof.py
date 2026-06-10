import json

from dataclasses import replace

from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)

from epics.epic075_signed_veracity_proofs.proof_envelope import (
    build_unsigned_envelope,
)

from epics.epic075_signed_veracity_proofs.proof_signer import (
    sign_envelope,
)

from epics.epic075_signed_veracity_proofs.proof_signature_verifier import (
    verify_signature,
)


def test_end_to_end_signed_proof_flow():

    runtime = VeracityRuntime()

    proof = runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )

    envelope = build_unsigned_envelope(
        proof
    )

    signed = sign_envelope(
        envelope
    )

    assert verify_signature(
        signed
    ) is True

    exported = signed.to_canonical_json()

    payload = json.loads(
        exported
    )

    assert payload["signature"] is not None

    assert payload["verified"] is True


def test_end_to_end_signed_proof_detects_tampering():

    runtime = VeracityRuntime()

    proof = runtime.prove(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "input-001"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "evidence-001"},
        governance={"schema_version": "1.0"},
    )

    envelope = build_unsigned_envelope(
        proof
    )

    signed = sign_envelope(
        envelope
    )

    tampered_payload = dict(
        signed.open_vce_payload
    )

    tampered_payload["identity"] = {
        "identity_id": "tampered"
    }

    tampered = replace(
        signed,
        open_vce_payload=tampered_payload,
    )

    assert verify_signature(
        tampered
    ) is False
