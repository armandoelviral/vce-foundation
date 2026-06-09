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


def build_signed_envelope():

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

    return sign_envelope(
        envelope
    )


def test_tamper_detection_rejects_modified_payload():

    signed = build_signed_envelope()

    tampered_payload = dict(
        signed.open_vce_payload
    )

    tampered_payload["identity"] = {
        "identity_id": "id-tampered"
    }

    tampered = replace(
        signed,
        open_vce_payload=tampered_payload,
    )

    assert verify_signature(
        tampered
    ) is False


def test_tamper_detection_accepts_untouched_payload():

    signed = build_signed_envelope()

    assert verify_signature(
        signed
    ) is True
