from datetime import datetime
import json
import re

from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION,
)
from sp001.contracts.knowledge_lexical_match import KnowledgeLexicalMatchStatus
from sp001.contracts.knowledge_lexical_ordering_evidence import (
    KNOWLEDGE_LEXICAL_ORDERING_POLICY,
)
from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeScopeMatchStatus,
    KnowledgeScopeMismatchReason,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
    KnowledgeRetrievalExclusionReason,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeTemporalApplicabilityStatus,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
)
from sp001.contracts.knowledge_source_status import (
    KnowledgeEvidenceStatus,
    KnowledgeLifecycleStatus,
)
from sp001.services.knowledge_lexical_text_normalization import (
    KNOWLEDGE_LEXICAL_NORMALIZATION_POLICY,
    normalize_knowledge_lexical_text,
)


_STRING = object()
_BOOL = object()
_UINT = object()
_POSINT = object()
_TIME = object()
_NULL_TIME = object()
_NULL_STRING = object()
_DIGEST = object()


def _enum_values(enum_type) -> frozenset[str]:
    return frozenset(member.value for member in enum_type)


DIGEST = {"algorithm": frozenset(("SHA-256",)), "value": _DIGEST}
IDENTITY = {
    "source_id": _STRING,
    "source_version": _STRING,
    "source_content_digest": DIGEST,
}
SELECTION = {"mode": _enum_values(KnowledgeScopeMode), "ids": [_STRING]}
SCOPE = {
    "organization_id": _STRING,
    "customer_id": _STRING,
    "jurisdiction": _STRING,
    "commercial_channel_id": _STRING,
    "document_type": _enum_values(KnowledgeDocumentType),
    "point_of_sale_scope": SELECTION,
    "department_scope": SELECTION,
    "campaign_id": _NULL_STRING,
}
STATUS = {
    "status_record_id": _STRING,
    "status_version": _POSINT,
    "identity": IDENTITY,
    "scope": SCOPE,
    "lifecycle_status": _enum_values(KnowledgeLifecycleStatus),
    "evidence_status": _enum_values(KnowledgeEvidenceStatus),
}
CONTEXT = {
    "organization_id": _STRING,
    "customer_id": _STRING,
    "jurisdiction": _STRING,
    "commercial_channel_id": _STRING,
    "document_type": _enum_values(KnowledgeDocumentType),
    "point_of_sale_id": _STRING,
    "department_id": _STRING,
    "campaign_id": _NULL_STRING,
    "evaluated_at": _TIME,
}
SCOPE_EVALUATION = {
    "source_scope": SCOPE,
    "retrieval_context": CONTEXT,
    "match_status": _enum_values(KnowledgeScopeMatchStatus),
    "mismatch_reasons": [_enum_values(KnowledgeScopeMismatchReason)],
}
EFFECTIVE_PERIOD = {
    "source_status": STATUS,
    "effective_from": _TIME,
    "effective_until": _NULL_TIME,
}
TEMPORAL_EVALUATION = {
    "effective_period": EFFECTIVE_PERIOD,
    "evaluated_at": _TIME,
    "temporal_status": _enum_values(KnowledgeTemporalApplicabilityStatus),
}
DECISION = {
    "source_status": STATUS,
    "retrieval_context": CONTEXT,
    "content_bytes_match_digest": _BOOL,
    "scope_evaluation": SCOPE_EVALUATION,
    "temporal_evaluation": TEMPORAL_EVALUATION,
    "verified_authority_binding_ids": [_STRING],
    "supersession_ids": [_STRING],
    "decision_status": _enum_values(KnowledgeRetrievalDecisionStatus),
    "exclusion_reasons": [_enum_values(KnowledgeRetrievalExclusionReason)],
}
CANDIDATE = {"candidate_id": _STRING, "decision": DECISION}
MANIFEST = {"retrieval_context": CONTEXT, "candidate_decisions": [CANDIDATE]}
QUERY = {
    "query_id": _STRING,
    "raw_text": _STRING,
    "normalized_text": _STRING,
    "terms": [_STRING],
    "normalization_policy": frozenset((KNOWLEDGE_LEXICAL_NORMALIZATION_POLICY,)),
}
TERM = {
    "query_term_index": _UINT,
    "term": _STRING,
    "occurrence_count": _UINT,
}
MATCH = {
    "query": QUERY,
    "candidate_id": _STRING,
    "source_identity": IDENTITY,
    "term_evidence": [TERM],
    "match_status": _enum_values(KnowledgeLexicalMatchStatus),
}
EVIDENCE = {
    "match": MATCH,
    "status_precedence": _UINT,
    "present_query_term_count": _UINT,
    "total_occurrence_count": _UINT,
    "ordering_key": [_UINT],
    "ordering_policy": frozenset((KNOWLEDGE_LEXICAL_ORDERING_POLICY,)),
}
ENTRY = {
    "declared_candidate_index": _UINT,
    "ordered_candidate_index": _UINT,
    "evidence": EVIDENCE,
}
ORDERING = {
    "query": QUERY,
    "entries": [ENTRY],
    "ordering_policy": frozenset((KNOWLEDGE_LEXICAL_ORDERING_POLICY,)),
}
COUNTS = {
    "candidate_count": _UINT,
    "included_candidate_count": _UINT,
    "excluded_candidate_count": _UINT,
    "ordered_candidate_count": _UINT,
}
ROOT = {
    "schema_version": _POSINT,
    "counts": COUNTS,
    "result": {"query": QUERY, "manifest": MANIFEST, "lexical_ordering": ORDERING},
}


def validate_knowledge_governed_retrieval_evidence_payload(*, payload: str) -> bool:
    """Validate received payload structure without asserting integrity."""
    if not isinstance(payload, str):
        raise TypeError("payload must be a string")
    if not payload.strip():
        raise ValueError("payload must not be empty")
    try:
        document = json.loads(
            payload,
            object_pairs_hook=_unique_object,
        )
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError("payload must contain valid JSON") from error
    _validate(value=document, specification=ROOT, path="retrieval evidence")
    if document["schema_version"] != KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION:
        raise ValueError("schema_version must equal supported version 1")
    _validate_query(document["result"]["query"])
    _validate_manifest(document)
    _validate_ordering(document)
    return True


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    document = {}
    for key, value in pairs:
        if key in document:
            raise ValueError(f"duplicate JSON field: {key}")
        document[key] = value
    return document


def _validate(*, value: object, specification: object, path: str) -> None:
    if isinstance(specification, dict):
        if not isinstance(value, dict):
            raise ValueError(f"{path} must be a JSON object")
        expected, present = frozenset(specification), frozenset(value)
        missing, unexpected = expected - present, present - expected
        if missing:
            raise ValueError(f"missing required {path} fields: " + ", ".join(sorted(missing)))
        if unexpected:
            raise ValueError(f"unexpected {path} fields: " + ", ".join(sorted(unexpected)))
        for field, nested in specification.items():
            _validate(value=value[field], specification=nested, path=f"{path}.{field}")
        return
    if isinstance(specification, list):
        if not isinstance(value, list):
            raise ValueError(f"{path} must be a JSON array")
        for index, nested in enumerate(value):
            _validate(value=nested, specification=specification[0], path=f"{path}[{index}]")
        return
    if isinstance(specification, frozenset):
        if not isinstance(value, str) or value not in specification:
            raise ValueError(f"{path} contains unsupported value")
        return
    if specification is _STRING:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{path} must be a non-empty string")
        return
    if specification is _NULL_STRING:
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{path} must be null or a non-empty string")
        return
    if specification is _BOOL:
        if type(value) is not bool:
            raise ValueError(f"{path} must be a boolean")
        return
    if specification in (_UINT, _POSINT):
        minimum = 0 if specification is _UINT else 1
        if type(value) is not int or value < minimum:
            label = "non-negative" if minimum == 0 else "positive"
            raise ValueError(f"{path} must be a {label} integer")
        return
    if specification in (_TIME, _NULL_TIME):
        if specification is _NULL_TIME and value is None:
            return
        _validate_timestamp(value=value, path=path)
        return
    if specification is _DIGEST:
        if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
            raise ValueError(f"{path} must contain 64 lowercase hexadecimal characters")
        return
    raise RuntimeError(f"unsupported validation specification for {path}")


def _validate_timestamp(*, value: object, path: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{path} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{path} must be an ISO-8601 timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{path} must include a UTC offset")


def _validate_query(query: dict) -> None:
    normalized = normalize_knowledge_lexical_text(text=query["raw_text"])
    if query["normalized_text"] != normalized:
        raise ValueError("normalized_text must match normalization policy")
    if query["terms"] != normalized.split(" "):
        raise ValueError("terms must match normalized_text positions")


def _validate_manifest(document: dict) -> None:
    result, counts = document["result"], document["counts"]
    manifest = result["manifest"]
    candidates = manifest["candidate_decisions"]
    candidate_ids = [item["candidate_id"] for item in candidates]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("candidate_id values must be unique")
    included = [item for item in candidates if item["decision"]["decision_status"] == "INCLUDED"]
    excluded = [item for item in candidates if item["decision"]["decision_status"] == "EXCLUDED"]
    expected_counts = {
        "candidate_count": len(candidates),
        "included_candidate_count": len(included),
        "excluded_candidate_count": len(excluded),
        "ordered_candidate_count": len(result["lexical_ordering"]["entries"]),
    }
    if counts != expected_counts:
        raise ValueError("counts must reconcile with manifest and ordering")
    context = manifest["retrieval_context"]
    for candidate in candidates:
        decision = candidate["decision"]
        if decision["retrieval_context"] != context:
            raise ValueError("decision retrieval_context must match manifest")
        if decision["scope_evaluation"]["retrieval_context"] != context:
            raise ValueError("scope evaluation context must match manifest")
        if decision["scope_evaluation"]["source_scope"] != decision["source_status"]["scope"]:
            raise ValueError("scope evaluation source must match source status")
        if decision["temporal_evaluation"]["effective_period"]["source_status"] != decision["source_status"]:
            raise ValueError("effective period source must match source status")
        if decision["temporal_evaluation"]["evaluated_at"] != context["evaluated_at"]:
            raise ValueError("temporal evaluation time must match context")
        if decision["decision_status"] == "INCLUDED" and decision["exclusion_reasons"]:
            raise ValueError("included decision must have no exclusion reasons")
        if decision["decision_status"] == "EXCLUDED" and not decision["exclusion_reasons"]:
            raise ValueError("excluded decision must declare exclusion reasons")


def _validate_ordering(document: dict) -> None:
    result = document["result"]
    query, ordering = result["query"], result["lexical_ordering"]
    entries = ordering["entries"]
    if ordering["query"] != query:
        raise ValueError("lexical ordering query must match result query")
    included = [item for item in result["manifest"]["candidate_decisions"] if item["decision"]["decision_status"] == "INCLUDED"]
    included_by_id = {item["candidate_id"]: item for item in included}
    ordered_ids = [entry["evidence"]["match"]["candidate_id"] for entry in entries]
    if len(ordered_ids) != len(set(ordered_ids)) or set(ordered_ids) != set(included_by_id):
        raise ValueError("ordering must contain every included candidate once")
    if [entry["ordered_candidate_index"] for entry in entries] != list(range(len(entries))):
        raise ValueError("ordered_candidate_index must be contiguous")
    declared = [entry["declared_candidate_index"] for entry in entries]
    if len(declared) != len(set(declared)) or set(declared) != set(range(len(entries))):
        raise ValueError("declared_candidate_index values must be contiguous")
    for previous, current in zip(entries, entries[1:]):
        previous_key = previous["evidence"]["ordering_key"]
        current_key = current["evidence"]["ordering_key"]
        if previous_key < current_key:
            raise ValueError("ordering_key values must be descending")
        if (
            previous_key == current_key
            and previous["declared_candidate_index"]
            > current["declared_candidate_index"]
        ):
            raise ValueError("equal ordering keys must preserve declared order")
    for entry in entries:
        evidence, match = entry["evidence"], entry["evidence"]["match"]
        candidate = included_by_id[match["candidate_id"]]
        if match["query"] != query:
            raise ValueError("lexical match query must match result query")
        if match["source_identity"] != candidate["decision"]["source_status"]["identity"]:
            raise ValueError("lexical source must match manifest source")
        terms, observed = query["terms"], match["term_evidence"]
        if len(observed) != len(terms):
            raise ValueError("term evidence must cover every query term")
        if [item["query_term_index"] for item in observed] != list(range(len(terms))):
            raise ValueError("query_term_index must be contiguous")
        if [item["term"] for item in observed] != terms:
            raise ValueError("term evidence must preserve query positions")
        present = sum(item["occurrence_count"] > 0 for item in observed)
        total = sum(item["occurrence_count"] for item in observed)
        status = "ALL_TERMS_PRESENT" if present == len(terms) else ("SOME_TERMS_PRESENT" if present else "NO_TERMS_PRESENT")
        precedence = {"ALL_TERMS_PRESENT": 2, "SOME_TERMS_PRESENT": 1, "NO_TERMS_PRESENT": 0}[status]
        if match["match_status"] != status:
            raise ValueError("match_status must reconcile with term evidence")
        if (
            evidence["present_query_term_count"] != present
            or evidence["total_occurrence_count"] != total
            or evidence["status_precedence"] != precedence
            or evidence["ordering_key"] != [precedence, present, total]
        ):
            raise ValueError("ordering evidence must reconcile with term evidence")
