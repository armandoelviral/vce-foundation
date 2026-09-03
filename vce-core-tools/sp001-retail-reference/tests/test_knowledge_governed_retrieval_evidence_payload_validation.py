import ast
import copy
import json

from pathlib import Path

import pytest

import sp001.services.knowledge_governed_retrieval_evidence_payload_validation as validator_module
from sp001.services.knowledge_governed_retrieval_evidence_payload_validation import (
    validate_knowledge_governed_retrieval_evidence_payload,
)
from sp001.services.knowledge_governed_retrieval_evidence_serialization import (
    serialize_knowledge_governed_retrieval_evidence,
)
from test_knowledge_governed_retrieval_evidence_serialization import (
    create_mixed_evidence,
)


def create_payload() -> str:
    return serialize_knowledge_governed_retrieval_evidence(
        evidence=create_mixed_evidence(
            raw_text="governed governed planogram",
        ),
    )


def create_document() -> dict:
    return json.loads(create_payload())


def encode(document: object) -> str:
    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def validate_document(document: object) -> bool:
    return validate_knowledge_governed_retrieval_evidence_payload(
        payload=encode(document),
    )


def first_decision(document: dict) -> dict:
    return document["result"]["manifest"]["candidate_decisions"][0]["decision"]


def first_entry(document: dict) -> dict:
    return document["result"]["lexical_ordering"]["entries"][0]


def test_valid_canonical_payload_passes() -> None:
    assert validate_knowledge_governed_retrieval_evidence_payload(
        payload=create_payload(),
    )
    payload = json.dumps(
        create_document(),
        indent=2,
        ensure_ascii=False,
    )
    assert validate_knowledge_governed_retrieval_evidence_payload(
        payload=payload,
    )


@pytest.mark.parametrize("invalid_payload", (None, {}, (), b"{}", 1))
def test_non_string_payload_is_rejected(invalid_payload: object) -> None:
    with pytest.raises(TypeError, match="payload must be a string"):
        validate_knowledge_governed_retrieval_evidence_payload(
            payload=invalid_payload,
        )


@pytest.mark.parametrize("empty_payload", ("", " ", "\n", "\t"))
def test_empty_payload_is_rejected(empty_payload: str) -> None:
    with pytest.raises(ValueError, match="payload must not be empty"):
        validate_knowledge_governed_retrieval_evidence_payload(
            payload=empty_payload,
        )


def test_malformed_json_is_rejected() -> None:
    with pytest.raises(ValueError, match="valid JSON"):
        validate_knowledge_governed_retrieval_evidence_payload(payload="{")


@pytest.mark.parametrize("document", ([], None, "evidence", 1, True))
def test_non_object_root_is_rejected(document: object) -> None:
    with pytest.raises(ValueError, match="JSON object"):
        validate_document(document)


@pytest.mark.parametrize("field", ("schema_version", "counts", "result"))
def test_missing_root_fields_are_rejected(field: str) -> None:
    document = create_document()
    del document[field]
    with pytest.raises(ValueError, match="missing required"):
        validate_document(document)


def test_unexpected_fields_are_rejected_at_every_level() -> None:
    documents = []
    root = create_document()
    root["digest"] = "unsupported"
    documents.append(root)
    nested = create_document()
    nested["result"]["query"]["authority"] = "unsupported"
    documents.append(nested)
    leaf = create_document()
    first_entry(leaf)["evidence"]["match"]["term_evidence"][0]["score"] = 1
    documents.append(leaf)
    for document in documents:
        with pytest.raises(ValueError, match="unexpected"):
            validate_document(document)


@pytest.mark.parametrize("version", (None, True, False, 0, 2, "1"))
def test_unsupported_schema_versions_are_rejected(version: object) -> None:
    document = create_document()
    document["schema_version"] = version
    with pytest.raises(ValueError):
        validate_document(document)


def test_boolean_and_integer_types_are_strict() -> None:
    boolean_document = create_document()
    first_decision(boolean_document)["content_bytes_match_digest"] = 1
    with pytest.raises(ValueError, match="boolean"):
        validate_document(boolean_document)
    integer_document = create_document()
    integer_document["counts"]["candidate_count"] = True
    with pytest.raises(ValueError, match="integer"):
        validate_document(integer_document)


def test_closed_vocabulary_values_are_rejected() -> None:
    document = create_document()
    first_decision(document)["decision_status"] = "AUTHORIZED"
    with pytest.raises(ValueError, match="unsupported value"):
        validate_document(document)


def test_invalid_timestamps_and_digests_are_rejected() -> None:
    timestamp_document = create_document()
    timestamp_document["result"]["manifest"]["retrieval_context"]["evaluated_at"] = "2026-03-15T12:00:00"
    with pytest.raises(ValueError, match="UTC offset"):
        validate_document(timestamp_document)
    digest_document = create_document()
    first_decision(digest_document)["source_status"]["identity"]["source_content_digest"]["value"] = "ABC"
    with pytest.raises(ValueError, match="lowercase hexadecimal"):
        validate_document(digest_document)


def test_query_normalization_and_term_positions_are_reconciled() -> None:
    normalized_document = create_document()
    normalized_document["result"]["query"]["normalized_text"] = "altered"
    with pytest.raises(ValueError, match="normalization policy"):
        validate_document(normalized_document)
    terms_document = create_document()
    terms_document["result"]["query"]["terms"].reverse()
    with pytest.raises(ValueError, match="terms must match"):
        validate_document(terms_document)


def test_summary_counts_are_reconciled() -> None:
    document = create_document()
    document["counts"]["included_candidate_count"] += 1
    with pytest.raises(ValueError, match="counts must reconcile"):
        validate_document(document)


def test_candidate_id_values_are_unique() -> None:
    document = create_document()
    candidates = document["result"]["manifest"]["candidate_decisions"]
    candidates[1]["candidate_id"] = candidates[0]["candidate_id"]
    with pytest.raises(ValueError, match="candidate_id values must be unique"):
        validate_document(document)


def test_manifest_nested_context_scope_and_status_are_reconciled() -> None:
    mutations = []
    context = create_document()
    first_decision(context)["retrieval_context"]["customer_id"] = "OTHER"
    mutations.append(context)
    scope = create_document()
    first_decision(scope)["scope_evaluation"]["source_scope"]["jurisdiction"] = "OTHER"
    mutations.append(scope)
    status = create_document()
    first_decision(status)["temporal_evaluation"]["effective_period"]["source_status"]["status_version"] = 2
    mutations.append(status)
    for document in mutations:
        with pytest.raises(ValueError, match="must match"):
            validate_document(document)


def test_inclusion_and_exclusion_reasons_are_reconciled() -> None:
    included = create_document()
    first_decision(included)["exclusion_reasons"] = ["SCOPE_MISMATCH"]
    with pytest.raises(ValueError, match="included decision"):
        validate_document(included)
    excluded = create_document()
    excluded_decision = excluded["result"]["manifest"]["candidate_decisions"][1]["decision"]
    excluded_decision["exclusion_reasons"] = []
    with pytest.raises(ValueError, match="excluded decision"):
        validate_document(excluded)


def test_ordering_covers_each_included_candidate_once() -> None:
    document = create_document()
    document["result"]["lexical_ordering"]["entries"] = []
    document["counts"]["ordered_candidate_count"] = 0
    with pytest.raises(ValueError, match="every included candidate once"):
        validate_document(document)


def test_ordering_indexes_and_stable_order_are_reconciled() -> None:
    index_document = create_document()
    first_entry(index_document)["ordered_candidate_index"] = 2
    with pytest.raises(ValueError, match="ordered_candidate_index"):
        validate_document(index_document)
    two = create_document()
    entry = copy.deepcopy(first_entry(two))
    entry["evidence"]["match"]["candidate_id"] = "CANDIDATE-EXCLUDED"
    two["result"]["lexical_ordering"]["entries"].append(entry)
    with pytest.raises(ValueError):
        validate_document(two)


def test_lexical_query_identity_positions_counts_and_key_are_reconciled() -> None:
    mutations = []
    query = create_document()
    first_entry(query)["evidence"]["match"]["query"]["query_id"] = "OTHER"
    mutations.append(query)
    position = create_document()
    first_entry(position)["evidence"]["match"]["term_evidence"][0]["query_term_index"] = 4
    mutations.append(position)
    count = create_document()
    first_entry(count)["evidence"]["total_occurrence_count"] += 1
    mutations.append(count)
    key = create_document()
    first_entry(key)["evidence"]["ordering_key"] = [0, 0, 0]
    mutations.append(key)
    for document in mutations:
        with pytest.raises(ValueError):
            validate_document(document)


def test_validator_does_not_mutate_received_document_or_claim_integrity() -> None:
    document = create_document()
    before = copy.deepcopy(document)
    assert validate_document(document)
    assert document == before
    source = Path(validator_module.__file__).read_text(encoding="UTF-8")
    tree = ast.parse(source)
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert not ({"hashlib", "hmac"} & imported)
    assert "compare_digest" not in source
    assert "deserialize" not in source
