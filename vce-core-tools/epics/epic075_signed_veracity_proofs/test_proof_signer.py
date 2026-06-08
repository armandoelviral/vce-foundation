from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)

from epics.epic075_signed_veracity_proofs.proof_envelope import (
    build_unsigned_envelope,
)

from epics.epic075_signed_veracity_proofs.proof_signer import (
    sign_envelope,
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


def test_signer_adds_signature():

    envelope = build_envelope()

    signed = sign_envelope(
        envelope
    )

    assert signed.signature is not None


def test_signer_adds_key_id():

    envelope = build_envelope()

    signed = sign_envelope(
        envelope
    )

    assert signed.signing_key_id == (
        "runtime-dev-key"
    )


def test_signer_is_deterministic():

    envelope = build_envelope()

    signed_a = sign_envelope(
        envelope
    )

    signed_b = sign_envelope(
        envelope
    )

    assert (
        signed_a.signature
        ==
        signed_b.signature
    )
