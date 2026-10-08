import inspect
import json

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_parsing import (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation import (
    stored_confirmation,
)


StoredConfirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation
)
parse_confirmation = (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation
)
serialize_confirmation = (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation
)


def stored_and_serialized():
    stored = stored_confirmation()
    serialization = serialize_confirmation(
        stored_confirmation=stored,
    )
    return stored, serialization


def canonical_document(
    value: dict[str, object],
) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def test_parser_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        parse_confirmation
    )

    assert tuple(signature.parameters) == (
        "serialization",
    )
    assert (
        signature.parameters["serialization"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert (
        signature.parameters["serialization"].annotation
        is str
    )
    assert signature.return_annotation is StoredConfirmation


def test_canonical_round_trip_is_exact() -> None:
    stored, serialization = stored_and_serialized()

    assert (
        parse_confirmation(
            serialization=serialization,
        )
        == stored
    )


def test_parser_returns_nominal_stored_confirmation() -> None:
    _, serialization = stored_and_serialized()

    parsed = parse_confirmation(
        serialization=serialization,
    )

    assert isinstance(
        parsed,
        StoredConfirmation,
    )


def test_complete_stored_graph_is_preserved() -> None:
    stored, serialization = stored_and_serialized()

    parsed = parse_confirmation(
        serialization=serialization,
    )

    assert parsed.storage_schema_version == (
        stored.storage_schema_version
    )
    assert parsed.participant_id == stored.participant_id
    assert parsed.decision == stored.decision
    assert parsed.publication_state == (
        stored.publication_state
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        b"",
        1,
        True,
        (),
        [],
        {},
    ),
)
def test_serialization_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="serialization must be a string",
    ):
        parse_confirmation(
            serialization=value,
        )


def test_empty_serialization_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="serialization must not be empty",
    ):
        parse_confirmation(
            serialization="",
        )


@pytest.mark.parametrize(
    "serialization",
    (
        "{",
        "[",
        "not-json",
        '"unterminated',
    ),
)
def test_invalid_json_is_rejected(
    serialization: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="valid JSON",
    ):
        parse_confirmation(
            serialization=serialization,
        )


@pytest.mark.parametrize(
    "serialization",
    (
        "[]",
        "null",
        "true",
        "1",
        '"text"',
    ),
)
def test_non_object_json_is_rejected(
    serialization: str,
) -> None:
    with pytest.raises(
        TypeError,
        match="JSON object",
    ):
        parse_confirmation(
            serialization=serialization,
        )


def test_duplicate_top_level_key_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    changed = serialization.replace(
        '"decision":',
        '"decision":"COMMIT","decision":',
        1,
    )

    with pytest.raises(
        ValueError,
        match="duplicate keys",
    ):
        parse_confirmation(
            serialization=changed,
        )


def test_duplicate_nested_key_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    changed = serialization.replace(
        '"phase":',
        '"phase":"COMMITTED","phase":',
        1,
    )

    with pytest.raises(
        ValueError,
        match="duplicate keys",
    ):
        parse_confirmation(
            serialization=changed,
        )


@pytest.mark.parametrize(
    "constant",
    (
        "NaN",
        "Infinity",
        "-Infinity",
    ),
)
def test_non_finite_json_constant_is_rejected(
    constant: str,
) -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["storage_schema_version"] = constant
    changed = canonical_document(document).replace(
        f'"storage_schema_version":"{constant}"',
        f'"storage_schema_version":{constant}',
        1,
    )

    with pytest.raises(
        ValueError,
        match="unsupported JSON constant",
    ):
        parse_confirmation(
            serialization=changed,
        )


def test_missing_top_level_key_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    del document["participant_id"]

    with pytest.raises(
        ValueError,
        match="exactly the supported keys",
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


def test_extra_top_level_key_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["extra"] = "value"

    with pytest.raises(
        ValueError,
        match="exactly the supported keys",
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


def test_wrong_domain_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["domain"] = "UNSUPPORTED"

    with pytest.raises(
        ValueError,
        match="domain is not supported",
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        [],
        "state",
        1,
        True,
    ),
)
def test_publication_state_requires_object(
    value: object,
) -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["publication_state"] = value

    with pytest.raises(
        TypeError,
        match="publication_state must be a JSON object",
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


def test_missing_publication_state_key_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    state = document["publication_state"]
    assert isinstance(state, dict)
    del state["signing_key_id"]

    with pytest.raises(
        ValueError,
        match="exactly the supported keys",
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


def test_extra_publication_state_key_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    state = document["publication_state"]
    assert isinstance(state, dict)
    state["extra"] = "value"

    with pytest.raises(
        ValueError,
        match="exactly the supported keys",
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        1,
        True,
        [],
        {},
    ),
)
def test_signature_hex_rejects_invalid_type(
    value: object,
) -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    state = document["publication_state"]
    assert isinstance(state, dict)
    state["signature_hex"] = value

    with pytest.raises(
        TypeError,
        match="signature_hex must be a string",
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


def test_signature_hex_rejects_empty_value() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    state = document["publication_state"]
    assert isinstance(state, dict)
    state["signature_hex"] = ""

    with pytest.raises(
        ValueError,
        match="signature_hex must not be empty",
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


@pytest.mark.parametrize(
    "value",
    (
        "0",
        "GG",
        "aaGG",
        "AA",
        "é0",
        "00 ",
    ),
)
def test_signature_hex_rejects_noncanonical_value(
    value: str,
) -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    state = document["publication_state"]
    assert isinstance(state, dict)
    state["signature_hex"] = value

    with pytest.raises(
        ValueError,
        match="canonical lowercase hexadecimal",
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        1,
        True,
        [],
        {},
        "1",
        "00000000000000000001 ",
        "0000000000000000000a",
        "００００００００００００００００００００１",
        "18446744073709551616",
    ),
)
def test_revision_rejects_noncanonical_value(
    value: object,
) -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    state = document["publication_state"]
    assert isinstance(state, dict)
    state["revision"] = value

    with pytest.raises(
        ValueError,
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


@pytest.mark.parametrize(
    "field",
    (
        "storage_schema_version",
        "participant_id",
        "decision",
    ),
)
def test_invalid_top_level_scalar_fails_closed(
    field: str,
) -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document[field] = None

    with pytest.raises(
        (TypeError, ValueError),
    ):
        parse_confirmation(
            serialization=canonical_document(document),
        )


def test_unsupported_top_level_schema_version_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["storage_schema_version"] = 2

    with pytest.raises(ValueError):
        parse_confirmation(
            serialization=canonical_document(document),
        )


def test_unsupported_nested_schema_version_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    state = document["publication_state"]
    assert isinstance(state, dict)
    state["storage_schema_version"] = 2

    with pytest.raises(ValueError):
        parse_confirmation(
            serialization=canonical_document(document),
        )


def test_noncanonical_whitespace_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    changed = json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
    )

    assert changed != serialization

    with pytest.raises(
        ValueError,
        match="serialization must be canonical",
    ):
        parse_confirmation(
            serialization=changed,
        )


def test_noncanonical_key_order_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    changed = json.dumps(
        dict(reversed(tuple(document.items()))),
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=False,
        separators=(",", ":"),
    )

    assert changed != serialization

    with pytest.raises(
        ValueError,
        match="serialization must be canonical",
    ):
        parse_confirmation(
            serialization=changed,
        )


def test_parser_does_not_deserialize_checkpoint() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    state = document["publication_state"]
    assert isinstance(state, dict)
    state["checkpoint_serialization"] = (
        "opaque-checkpoint"
    )
    changed = canonical_document(document)

    parsed = parse_confirmation(
        serialization=changed,
    )

    assert (
        parsed
        .publication_state
        .checkpoint_serialization
        == "opaque-checkpoint"
    )


def test_parser_is_deterministic() -> None:
    _, serialization = stored_and_serialized()

    first = parse_confirmation(
        serialization=serialization,
    )
    second = parse_confirmation(
        serialization=serialization,
    )

    assert first == second


def test_parser_defines_no_storage_or_participant_effects() -> None:
    source = inspect.getsource(
        parse_confirmation
    )

    assert "sqlite" not in source
    assert "open(" not in source
    assert ".read(" not in source
    assert ".write(" not in source
    assert ".prepare(" not in source
    assert ".commit(" not in source
    assert ".abort(" not in source


def test_parser_defines_no_signature_verification() -> None:
    source = inspect.getsource(
        parse_confirmation
    )

    assert "verify_security_admission" not in source
    assert "public_key(" not in source
