import inspect
import json
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation import (
    stored_confirmation,
    stored_state,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
StoredConfirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation
)
serialize = (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation
)
_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-PARTICIPANT-"
    "APPLICATION-CONFIRMATION"
)
_TOP_LEVEL_KEYS = {
    "decision",
    "domain",
    "participant_id",
    "publication_state",
    "storage_schema_version",
}
_STATE_KEYS = {
    "checkpoint_serialization",
    "phase",
    "public_key_encoding",
    "public_key_fingerprint",
    "publication_id",
    "revision",
    "signature_encoding",
    "signature_hex",
    "signing_algorithm",
    "signing_key_id",
    "storage_schema_version",
}


def serialized(
    *,
    decision: Decision = Decision.COMMIT,
    participant_id: str = "participant-001",
    revision: int = 4,
):
    state = stored_state(
        phase=(
            Phase.COMMITTED
            if decision is Decision.COMMIT
            else Phase.ABORTED
        ),
        revision=revision,
    )
    value = stored_confirmation(
        participant_id=participant_id,
        decision=decision,
        state=state,
    )
    return (
        value,
        serialize(
            stored_confirmation=value,
        ),
    )


def test_serialization_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        serialize
    )

    assert tuple(signature.parameters) == (
        "stored_confirmation",
    )
    assert (
        signature.parameters["stored_confirmation"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert (
        signature.parameters["stored_confirmation"].annotation
        is StoredConfirmation
    )
    assert signature.return_annotation is str


def test_serialization_returns_string() -> None:
    _, value = serialized()

    assert type(value) is str


def test_document_has_exact_top_level_keys() -> None:
    _, value = serialized()
    document = json.loads(value)

    assert set(document) == _TOP_LEVEL_KEYS


def test_document_has_exact_state_keys() -> None:
    _, value = serialized()
    document = json.loads(value)

    assert (
        set(document["publication_state"])
        == _STATE_KEYS
    )


def test_domain_is_exact() -> None:
    _, value = serialized()

    assert json.loads(value)["domain"] == _DOMAIN


def test_storage_schema_version_is_preserved() -> None:
    source, value = serialized()

    assert (
        json.loads(value)["storage_schema_version"]
        == source.storage_schema_version
    )


def test_participant_identifier_is_preserved() -> None:
    _, value = serialized(
        participant_id="participant/opaque",
    )

    assert (
        json.loads(value)["participant_id"]
        == "participant/opaque"
    )


@pytest.mark.parametrize(
    "decision",
    (
        Decision.COMMIT,
        Decision.ABORT,
    ),
)
def test_decision_is_preserved(
    decision: Decision,
) -> None:
    _, value = serialized(
        decision=decision,
    )

    assert (
        json.loads(value)["decision"]
        == decision.value
    )


def test_complete_publication_state_is_preserved() -> None:
    source, value = serialized()
    state = json.loads(value)["publication_state"]
    retained = source.publication_state

    assert state == {
        "checkpoint_serialization": (
            retained.checkpoint_serialization
        ),
        "phase": retained.phase,
        "public_key_encoding": (
            retained.public_key_encoding
        ),
        "public_key_fingerprint": (
            retained.public_key_fingerprint
        ),
        "publication_id": (
            retained.publication_id
        ),
        "revision": (
            f"{retained.revision:020d}"
        ),
        "signature_encoding": (
            retained.signature_encoding
        ),
        "signature_hex": (
            retained.signature.hex()
        ),
        "signing_algorithm": (
            retained.signing_algorithm
        ),
        "signing_key_id": (
            retained.signing_key_id
        ),
        "storage_schema_version": (
            retained.storage_schema_version
        ),
    }


@pytest.mark.parametrize(
    ("revision", "encoded"),
    (
        (
            1,
            "00000000000000000001",
        ),
        (
            4,
            "00000000000000000004",
        ),
        (
            2**32,
            "00000000004294967296",
        ),
        (
            2**64 - 1,
            "18446744073709551615",
        ),
    ),
)
def test_revision_uses_exact_twenty_digit_encoding(
    revision: int,
    encoded: str,
) -> None:
    _, value = serialized(
        revision=revision,
    )

    assert (
        json.loads(value)
        ["publication_state"]
        ["revision"]
        == encoded
    )


def test_signature_uses_lowercase_hexadecimal() -> None:
    source, value = serialized()
    signature_hex = (
        json.loads(value)
        ["publication_state"]
        ["signature_hex"]
    )

    assert signature_hex == (
        source.publication_state.signature.hex()
    )
    assert signature_hex == signature_hex.lower()
    assert bytes.fromhex(signature_hex) == (
        source.publication_state.signature
    )


def test_checkpoint_json_remains_embedded_text() -> None:
    source, value = serialized()

    assert (
        json.loads(value)
        ["publication_state"]
        ["checkpoint_serialization"]
        == (
            source
            .publication_state
            .checkpoint_serialization
        )
    )


def test_serialization_is_canonical_json() -> None:
    _, value = serialized()
    document = json.loads(value)

    assert value == json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def test_serialization_is_deterministic() -> None:
    source = stored_confirmation()

    assert (
        serialize(
            stored_confirmation=source,
        )
        == serialize(
            stored_confirmation=source,
        )
    )


def test_non_ascii_text_is_escaped() -> None:
    _, value = serialized(
        participant_id="participante-é",
    )

    assert "é" not in value
    assert "\\u00e9" in value


def test_serialization_contains_no_incidental_whitespace() -> None:
    _, value = serialized()

    assert "\n" not in value
    assert ": " not in value
    assert ", " not in value


def test_serialization_does_not_mutate_source() -> None:
    source = stored_confirmation()
    before = repr(source)

    serialize(
        stored_confirmation=source,
    )

    assert repr(source) == before


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        1,
        "stored-confirmation",
        object(),
    ),
)
def test_serialization_rejects_invalid_nominal_value(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="stored_confirmation must be a",
    ):
        serialize(
            stored_confirmation=value,
        )


def test_serialization_revalidates_revision_boundary() -> None:
    source = stored_confirmation()
    changed_state = replace(
        source.publication_state,
        revision=2**64 - 1,
    )
    changed = replace(
        source,
        publication_state=changed_state,
    )

    value = serialize(
        stored_confirmation=changed,
    )

    assert (
        json.loads(value)
        ["publication_state"]
        ["revision"]
        == "18446744073709551615"
    )


def test_serialization_defines_no_storage_effects() -> None:
    source = inspect.getsource(
        serialize
    ).lower()

    assert "sqlite" not in source
    assert "database" not in source
    assert "open(" not in source
    assert ".write(" not in source


def test_serialization_defines_no_participant_effects() -> None:
    source = inspect.getsource(
        serialize
    )

    assert ".prepare(" not in source
    assert ".commit(" not in source
    assert ".abort(" not in source


def test_serialization_defines_no_signature_verification() -> None:
    source = inspect.getsource(
        serialize
    )

    assert "verify_security_admission" not in source
    assert "public_key.verify" not in source
