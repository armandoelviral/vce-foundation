import inspect
import json

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_parsing import (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)


StoredIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent
)


def stored_and_serialized(
    *,
    publication_id: str = "publication-001",
    scalar: int = 1,
):
    stored = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            publication_intent=create_intent(
                publication_id=publication_id,
                scalar=scalar,
            ),
        )
    )
    serialization = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=stored,
        )
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
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent
    )

    assert tuple(signature.parameters) == (
        "serialization",
    )
    assert (
        signature.parameters[
            "serialization"
        ].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert (
        signature.return_annotation
        is StoredIntent
    )


@pytest.mark.parametrize(
    "scalar",
    (
        1,
        2,
        3,
        5,
        8,
    ),
)
def test_canonical_round_trip_is_exact(
    scalar: int,
) -> None:
    stored, serialization = stored_and_serialized(
        scalar=scalar,
    )

    parsed = (
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=serialization,
        )
    )

    assert parsed == stored


@pytest.mark.parametrize(
    "publication_id",
    (
        "publication-001",
        "opaque/publication:value",
        "tenant:alpha:publication:42",
        "publicación-ñ",
    ),
)
def test_opaque_publication_identifier_round_trips(
    publication_id: str,
) -> None:
    stored, serialization = stored_and_serialized(
        publication_id=publication_id,
    )

    parsed = (
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=serialization,
        )
    )

    assert parsed.publication_id == publication_id
    assert parsed == stored


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        b"serialization",
        1,
        True,
        (),
        {},
    ),
)
def test_serialization_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="serialization",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=value,
        )


def test_empty_serialization_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization="",
        )


@pytest.mark.parametrize(
    "serialization",
    (
        "{",
        "[",
        "not-json",
    ),
)
def test_invalid_json_is_rejected(
    serialization: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="valid JSON",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=serialization,
        )


@pytest.mark.parametrize(
    "serialization",
    (
        "null",
        "true",
        "1",
        '"intent"',
        "[]",
    ),
)
def test_non_object_json_is_rejected(
    serialization: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="JSON object",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=serialization,
        )


def test_duplicate_key_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    changed = serialization.replace(
        '{"checkpoint_serialization":',
        '{"checkpoint_serialization":"duplicate",'
        '"checkpoint_serialization":',
        1,
    )

    with pytest.raises(
        ValueError,
        match="duplicate keys",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
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
    changed = serialization.replace(
        '"storage_schema_version":1',
        f'"storage_schema_version":{constant}',
    )

    with pytest.raises(
        ValueError,
        match="non-finite",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=changed,
        )


def test_missing_key_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    del document["signing_key_id"]

    with pytest.raises(
        ValueError,
        match="exactly the supported keys",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=canonical_document(document),
        )


def test_extra_key_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["unexpected"] = "value"

    with pytest.raises(
        ValueError,
        match="exactly the supported keys",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=canonical_document(document),
        )


def test_wrong_domain_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["domain"] = "OTHER-DOMAIN"

    with pytest.raises(
        ValueError,
        match="domain is not supported",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=canonical_document(document),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        1,
        True,
        (),
        {},
    ),
)
def test_signature_hex_rejects_invalid_type(
    value: object,
) -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["signature_hex"] = value

    with pytest.raises(
        TypeError,
        match="signature_hex",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=canonical_document(document),
        )


def test_signature_hex_rejects_empty_value() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["signature_hex"] = ""

    with pytest.raises(
        ValueError,
        match="signature_hex must not be empty",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
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
    document["signature_hex"] = value

    with pytest.raises(
        ValueError,
        match="canonical lowercase hexadecimal",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=canonical_document(document),
        )


def test_unsupported_schema_version_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["storage_schema_version"] = 2

    with pytest.raises(
        ValueError,
        match="storage_schema_version",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
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
        match="must be canonical",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=changed,
        )


def test_noncanonical_key_order_is_rejected() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    reversed_document = dict(
        reversed(tuple(document.items()))
    )
    changed = json.dumps(
        reversed_document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=False,
        separators=(",", ":"),
    )

    assert changed != serialization

    with pytest.raises(
        ValueError,
        match="must be canonical",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=changed,
        )


def test_parser_does_not_deserialize_checkpoint() -> None:
    _, serialization = stored_and_serialized()
    document = json.loads(serialization)
    document["checkpoint_serialization"] = "opaque-checkpoint"
    changed = canonical_document(document)

    parsed = (
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            serialization=changed,
        )
    )

    assert (
        parsed.checkpoint_serialization
        == "opaque-checkpoint"
    )


def test_parser_defines_no_storage_or_verification_effects() -> None:
    source = inspect.getsource(
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent
    )

    assert "sqlite" not in source
    assert "open(" not in source
    assert "verify_security_admission" not in source
    assert ".read(" not in source
    assert ".write(" not in source
