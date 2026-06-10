import json

from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)
from epics.epic075_signed_veracity_proofs.proof_envelope import (
    build_unsigned_envelope,
)
from epics.epic075_signed_veracity_proofs.proof_signer import (
    sign_envelope,
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

    return sign_envelope(
        build_unsigned_envelope(
            proof
        )
    )


def test_signed_proof_exports_as_valid_json():

    envelope = build_signed_envelope()

    exported = envelope.to_canonical_json()

    payload = json.loads(
        exported
    )

    assert payload["signature"] is not None
    assert payload["signing_key_id"] == "runtime-dev-key"


def test_signed_proof_export_contains_core_fields():

    envelope = build_signed_envelope()

    payload = json.loads(
        envelope.to_canonical_json()
    )

    assert "open_vce_payload" in payload
    assert "artifact_hash" in payload
    assert "ledger_sequence" in payload
    assert "verified" in payload
    assert "signature" in payload
    assert "signature_algorithm" in payload
