import json
from typing import NoReturn

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_parsing import (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_parsing import (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)


StoredEvidence = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence
)
_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-DECISION-EVIDENCE"
)
_SUPPORTED_STORAGE_SCHEMA_VERSION = 1
_TOP_LEVEL_KEYS = frozenset(
    (
        "decision_record",
        "domain",
        "publication_intent",
        "storage_schema_version",
    )
)


def parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
    *,
    serialization: str,
) -> StoredEvidence:
    """Parse strict canonical durable signed decision evidence."""

    if type(serialization) is not str:
        raise TypeError(
            "serialization must be a string"
        )
    if not serialization:
        raise ValueError(
            "serialization must not be empty"
        )

    try:
        document = json.loads(
            serialization,
            object_pairs_hook=_strict_json_object,
            parse_constant=_reject_json_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError(
            "serialization must contain valid JSON"
        ) from error

    if not isinstance(document, dict):
        raise ValueError(
            "serialization must contain a JSON object"
        )

    if frozenset(document) != _TOP_LEVEL_KEYS:
        raise ValueError(
            "stored decision evidence must contain "
            "exactly the supported keys"
        )

    if document["domain"] != _DOMAIN:
        raise ValueError(
            "stored decision evidence domain is not supported"
        )

    storage_schema_version = document[
        "storage_schema_version"
    ]
    if type(storage_schema_version) is not int:
        raise TypeError(
            "storage_schema_version must be an integer"
        )
    if (
        storage_schema_version
        != _SUPPORTED_STORAGE_SCHEMA_VERSION
    ):
        raise ValueError(
            "stored decision evidence uses an unsupported "
            "storage schema version"
        )

    publication_intent_serialization = (
        _canonical_nested_serialization(
            value=document["publication_intent"],
            field="publication_intent",
        )
    )
    decision_record_serialization = (
        _canonical_nested_serialization(
            value=document["decision_record"],
            field="decision_record",
        )
    )

    stored_evidence = StoredEvidence(
        publication_intent=(
            parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
                serialization=(
                    publication_intent_serialization
                ),
            )
        ),
        decision_record=(
            parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record(
                serialization=(
                    decision_record_serialization
                ),
            )
        ),
    )

    canonical = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=stored_evidence,
        )
    )
    if canonical != serialization:
        raise ValueError(
            "serialization must be canonical"
        )

    return stored_evidence


def _canonical_nested_serialization(
    *,
    value: object,
    field: str,
) -> str:
    if not isinstance(value, dict):
        raise TypeError(
            f"{field} must be a JSON object"
        )

    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _strict_json_object(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    document: dict[str, object] = {}

    for key, value in pairs:
        if key in document:
            raise ValueError(
                "serialization must not contain duplicate keys"
            )
        document[key] = value

    return document


def _reject_json_constant(
    value: str,
) -> NoReturn:
    raise ValueError(
        "serialization must not contain non-finite values"
    )
