import inspect
import json

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_parsing import (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_projection import (
    zero_preparation_abort,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_deserialization import (
    project_commit,
)


StoredEvidence = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence
)
_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-DECISION-EVIDENCE"
)


def commit_evidence_and_serialization(
    *,
    size: int = 3,
):
    decision_record, _ = project_commit(
        size=size,
    )
    evidence = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=decision_record,
        )
    )
    serialization = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=evidence,
        )
    )
    return evidence, serialization


def abort_evidence_and_serialization():
    evidence = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=zero_preparation_abort(),
        )
    )
    serialization = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=evidence,
        )
    )
    return evidence, serialization


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
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
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
        is StoredEvidence
    )


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        5,
        8,
    ),
)
def test_commit_round_trip_is_exact(
    size: int,
) -> None:
    evidence, serialization = (
        commit_evidence_and_serialization(
            size=size,
        )
    )

    parsed = (
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=serialization,
        )
    )

    assert parsed == evidence


def test_zero_preparation_abort_round_trip_is_exact() -> None:
    evidence, serialization = (
        abort_evidence_and_serialization()
    )

    parsed = (
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=serialization,
        )
    )

    assert parsed == evidence
    assert parsed.decision_record.decision == "ABORT"
    assert parsed.decision_record.preparations == ()
    assert (
        parsed.publication_intent.publication_id
        == parsed.decision_record.publication_id
    )


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
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=value,
        )


def test_empty_serialization_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
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
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=serialization,
        )


@pytest.mark.parametrize(
    "serialization",
    (
        "null",
        "true",
        "1",
        '"evidence"',
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
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=serialization,
        )


def test_duplicate_key_is_rejected() -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
    changed = serialization.replace(
        '{"decision_record":',
        '{"decision_record":{},'
        '"decision_record":',
        1,
    )

    with pytest.raises(
        ValueError,
        match="duplicate keys",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
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
def test_non_finite_constant_is_rejected(
    constant: str,
) -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
    changed = serialization.replace(
        '"storage_schema_version":1',
        f'"storage_schema_version":{constant}',
    )

    with pytest.raises(
        ValueError,
        match="non-finite",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=changed,
        )


def test_missing_top_level_key_is_rejected() -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
    document = json.loads(serialization)
    del document["publication_intent"]

    with pytest.raises(
        ValueError,
        match="exactly the supported keys",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=canonical_document(document),
        )


def test_extra_top_level_key_is_rejected() -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
    document = json.loads(serialization)
    document["unexpected"] = "value"

    with pytest.raises(
        ValueError,
        match="exactly the supported keys",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=canonical_document(document),
        )


def test_wrong_domain_is_rejected() -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
    document = json.loads(serialization)
    document["domain"] = "OTHER-DOMAIN"

    with pytest.raises(
        ValueError,
        match="domain is not supported",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=canonical_document(document),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        "1",
        1.0,
        True,
        (),
    ),
)
def test_schema_version_rejects_invalid_type(
    value: object,
) -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
    document = json.loads(serialization)
    document["storage_schema_version"] = value

    with pytest.raises(
        TypeError,
        match="storage_schema_version",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=canonical_document(document),
        )


@pytest.mark.parametrize(
    "version",
    (
        0,
        2,
        3,
    ),
)
def test_unsupported_schema_version_is_rejected(
    version: int,
) -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
    document = json.loads(serialization)
    document["storage_schema_version"] = version

    with pytest.raises(
        ValueError,
        match="unsupported storage schema version",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=canonical_document(document),
        )


@pytest.mark.parametrize(
    "field",
    (
        "publication_intent",
        "decision_record",
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        None,
        "object",
        1,
        True,
        (),
    ),
)
def test_nested_document_requires_object(
    field: str,
    value: object,
) -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
    document = json.loads(serialization)
    document[field] = value

    with pytest.raises(
        TypeError,
        match=field,
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=canonical_document(document),
        )


def test_different_publication_identifiers_are_rejected() -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
    document = json.loads(serialization)
    document["publication_intent"][
        "publication_id"
    ] = "different-publication"

    with pytest.raises(
        ValueError,
        match="same publication_id",
    ):
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=canonical_document(document),
        )


def test_noncanonical_whitespace_is_rejected() -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
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
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=changed,
        )


def test_noncanonical_key_order_is_rejected() -> None:
    _, serialization = (
        commit_evidence_and_serialization()
    )
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
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            serialization=changed,
        )


def test_parser_defines_no_storage_behavior() -> None:
    source = inspect.getsource(
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert "sqlite" not in source
    assert "open(" not in source
    assert ".read(" not in source
    assert ".write(" not in source


def test_parser_defines_no_decision_or_signature_verification() -> None:
    source = inspect.getsource(
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert "derive_security_admission" not in source
    assert "verify_security_admission" not in source
