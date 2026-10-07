import inspect
import json
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_parsing import (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    create_stored_record,
)


StoredDecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord
)
parse = (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record
)
serialize = (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record
)
UINT64_MAX = (1 << 64) - 1


def canonical(
    value: object,
) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def serialized_record(
    *,
    size: int = 3,
    decision: str = "COMMIT",
):
    record = create_stored_record(
        size=size,
        decision=decision,
    )
    return record, serialize(
        stored_record=record,
    )


@pytest.mark.parametrize(
    ("size", "decision"),
    (
        (1, "COMMIT"),
        (2, "COMMIT"),
        (3, "COMMIT"),
        (5, "COMMIT"),
        (1, "ABORT"),
        (3, "ABORT"),
    ),
)
def test_canonical_serialization_round_trips_exactly(
    size: int,
    decision: str,
) -> None:
    record, serialization = serialized_record(
        size=size,
        decision=decision,
    )

    assert parse(
        serialization=serialization,
    ) == record


def test_uint64_max_revision_round_trips_exactly() -> None:
    record = create_stored_record(
        size=1,
    )
    participant_id, state = record.preparations[0]
    changed = replace(
        record,
        preparations=(
            (
                participant_id,
                replace(
                    state,
                    revision=UINT64_MAX,
                ),
            ),
        ),
    )
    serialization = serialize(
        stored_record=changed,
    )

    assert parse(
        serialization=serialization,
    ) == changed


@pytest.mark.parametrize(
    "value",
    (
        None,
        b"{}",
        1,
        True,
        object(),
        (),
    ),
)
def test_serialization_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="serialization",
    ):
        parse(
            serialization=value,
        )


def test_empty_serialization_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        parse(
            serialization="",
        )


@pytest.mark.parametrize(
    "value",
    (
        "{",
        "not-json",
        '{"unterminated":',
    ),
)
def test_malformed_json_is_rejected(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="valid JSON",
    ):
        parse(
            serialization=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        "null",
        "[]",
        '"document"',
        "1",
        "true",
    ),
)
def test_top_level_requires_json_object(
    value: str,
) -> None:
    with pytest.raises(
        TypeError,
        match="decision document",
    ):
        parse(
            serialization=value,
        )


@pytest.mark.parametrize(
    "constant",
    (
        "NaN",
        "Infinity",
        "-Infinity",
    ),
)
def test_non_json_numeric_constant_is_rejected(
    constant: str,
) -> None:
    _, serialization = serialized_record()
    changed = serialization.replace(
        '"storage_schema_version":1',
        f'"storage_schema_version":{constant}',
        1,
    )

    with pytest.raises(
        ValueError,
        match="not supported",
    ):
        parse(
            serialization=changed,
        )


def test_duplicate_object_key_is_rejected() -> None:
    _, serialization = serialized_record()
    changed = serialization.replace(
        '{"decision":',
        '{"decision":"COMMIT","decision":',
        1,
    )

    with pytest.raises(
        ValueError,
        match="duplicate",
    ):
        parse(
            serialization=changed,
        )


def test_missing_top_level_key_is_rejected() -> None:
    _, serialization = serialized_record()
    value = json.loads(serialization)
    del value["decision"]

    with pytest.raises(
        ValueError,
        match="exact canonical keys",
    ):
        parse(
            serialization=canonical(value),
        )


def test_extra_top_level_key_is_rejected() -> None:
    _, serialization = serialized_record()
    value = json.loads(serialization)
    value["unexpected"] = True

    with pytest.raises(
        ValueError,
        match="exact canonical keys",
    ):
        parse(
            serialization=canonical(value),
        )


def test_wrong_domain_is_rejected() -> None:
    _, serialization = serialized_record()
    value = json.loads(serialization)
    value["domain"] = "OTHER-DOMAIN"

    with pytest.raises(
        ValueError,
        match="domain",
    ):
        parse(
            serialization=canonical(value),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        {},
        "participants",
        1,
        True,
    ),
)
def test_participant_ids_requires_json_array(
    value: object,
) -> None:
    _, serialization = serialized_record()
    document = json.loads(serialization)
    document["participant_ids"] = value

    with pytest.raises(
        TypeError,
        match="JSON array",
    ):
        parse(
            serialization=canonical(document),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        {},
        "preparations",
        1,
        True,
    ),
)
def test_preparations_requires_json_array(
    value: object,
) -> None:
    _, serialization = serialized_record()
    document = json.loads(serialization)
    document["preparations"] = value

    with pytest.raises(
        TypeError,
        match="JSON array",
    ):
        parse(
            serialization=canonical(document),
        )


def test_preparation_requires_exact_keys() -> None:
    _, serialization = serialized_record()
    document = json.loads(serialization)
    document["preparations"][0][
        "unexpected"
    ] = True

    with pytest.raises(
        ValueError,
        match="preparation.*exact canonical keys",
    ):
        parse(
            serialization=canonical(document),
        )


def test_publication_state_requires_json_object() -> None:
    _, serialization = serialized_record()
    document = json.loads(serialization)
    document["preparations"][0][
        "publication_state"
    ] = None

    with pytest.raises(
        TypeError,
        match="publication_state",
    ):
        parse(
            serialization=canonical(document),
        )


def test_publication_state_requires_exact_keys() -> None:
    _, serialization = serialized_record()
    document = json.loads(serialization)
    del document["preparations"][0][
        "publication_state"
    ]["phase"]

    with pytest.raises(
        ValueError,
        match="publication_state.*exact canonical keys",
    ):
        parse(
            serialization=canonical(document),
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
def test_signature_hex_requires_string(
    value: object,
) -> None:
    _, serialization = serialized_record()
    document = json.loads(serialization)
    document["preparations"][0][
        "publication_state"
    ]["signature_hex"] = value

    with pytest.raises(
        TypeError,
        match="signature_hex",
    ):
        parse(
            serialization=canonical(document),
        )


@pytest.mark.parametrize(
    "value",
    (
        "",
        "0",
        "GG",
        "ab cd",
        "AB",
        "áa",
    ),
)
def test_signature_hex_requires_canonical_lowercase_bytes(
    value: str,
) -> None:
    _, serialization = serialized_record()
    document = json.loads(serialization)
    document["preparations"][0][
        "publication_state"
    ]["signature_hex"] = value

    with pytest.raises(
        ValueError,
        match="lowercase hexadecimal",
    ):
        parse(
            serialization=canonical(document),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        1,
        True,
        "1",
        "0000000000000000001",
        "000000000000000000001",
        "０００００００００００００００００００１",
        "00000000000000000000",
        "99999999999999999999",
    ),
)
def test_revision_requires_canonical_positive_uint64(
    value: object,
) -> None:
    _, serialization = serialized_record()
    document = json.loads(serialization)
    document["preparations"][0][
        "publication_state"
    ]["revision"] = value

    with pytest.raises(
        (TypeError, ValueError),
    ):
        parse(
            serialization=canonical(document),
        )


@pytest.mark.parametrize(
    "mutation",
    (
        lambda value: json.dumps(
            value,
            ensure_ascii=True,
            sort_keys=True,
        ),
        lambda value: json.dumps(
            dict(reversed(tuple(value.items()))),
            ensure_ascii=True,
            sort_keys=False,
            separators=(",", ":"),
        ),
    ),
)
def test_noncanonical_json_representation_is_rejected(
    mutation,
) -> None:
    _, serialization = serialized_record()
    value = json.loads(serialization)
    changed = mutation(value)

    assert changed != serialization

    with pytest.raises(
        ValueError,
        match="canonical",
    ):
        parse(
            serialization=changed,
        )


def test_parse_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        parse
    )

    assert tuple(signature.parameters) == (
        "serialization",
    )
    parameter = signature.parameters[
        "serialization"
    ]
    assert (
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert parameter.annotation is str
    assert (
        signature.return_annotation
        is StoredDecisionRecord
    )


def test_parser_defines_no_domain_effect_or_persistence() -> None:
    source = inspect.getsource(
        parse
    ).lower()

    for forbidden in (
        "sqlite",
        "database",
        "open(",
        "write(",
        ".prepare(",
        ".commit(",
        ".abort(",
        "network",
        "http",
        "socket",
        "pickle",
    ):
        assert forbidden not in source
