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


def test_signature_verification_accepts_valid_signature():

    envelope = build_signed_envelope()

    assert verify_signature(
        envelope
    ) is True


def test_signature_verification_rejects_unsigned_envelope():

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

    assert verify_signature(
        envelope
    ) is False
