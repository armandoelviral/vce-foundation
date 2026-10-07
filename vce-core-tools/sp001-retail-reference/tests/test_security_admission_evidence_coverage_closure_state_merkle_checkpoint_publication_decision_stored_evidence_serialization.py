import inspect
import json

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
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


def commit_stored_evidence(
    *,
    size: int = 3,
) -> StoredEvidence:
    decision_record, _ = project_commit(
        size=size,
    )
    return (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=decision_record,
        )
    )


def serialize(
    *,
    size: int = 3,
) -> str:
    return (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=commit_stored_evidence(
                size=size,
            ),
        )
    )


def test_serialization_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert tuple(signature.parameters) == (
        "stored_evidence",
    )
    assert (
        signature.parameters[
            "stored_evidence"
        ].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert signature.return_annotation is str


def test_serialization_has_exact_top_level_keys() -> None:
    document = json.loads(serialize())

    assert set(document) == {
        "decision_record",
        "domain",
        "publication_intent",
        "storage_schema_version",
    }


def test_domain_and_schema_version_are_exact() -> None:
    document = json.loads(serialize())

    assert document["domain"] == _DOMAIN
    assert document["storage_schema_version"] == 1
    assert type(
        document["storage_schema_version"]
    ) is int


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
def test_commit_evidence_preserves_both_nested_documents(
    size: int,
) -> None:
    evidence = commit_stored_evidence(
        size=size,
    )
    serialization = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=evidence,
        )
    )
    document = json.loads(serialization)

    expected_intent = json.loads(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=evidence.publication_intent,
        )
    )
    expected_decision = json.loads(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record(
            stored_record=evidence.decision_record,
        )
    )

    assert (
        document["publication_intent"]
        == expected_intent
    )
    assert (
        document["decision_record"]
        == expected_decision
    )


def test_zero_preparation_abort_retains_complete_intent() -> None:
    decision_record = zero_preparation_abort()
    evidence = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=decision_record,
        )
    )

    document = json.loads(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=evidence,
        )
    )

    assert (
        document["decision_record"]["decision"]
        == "ABORT"
    )
    assert (
        document["decision_record"]["preparations"]
        == []
    )
    assert (
        document["publication_intent"][
            "publication_id"
        ]
        == decision_record.publication_intent.publication_id
    )
    assert (
        bytes.fromhex(
            document["publication_intent"][
                "signature_hex"
            ]
        )
        == (
            decision_record
            .publication_intent
            .checkpoint_signature
            .signature
        )
    )


def test_nested_publication_identifiers_are_exactly_equal() -> None:
    document = json.loads(serialize())

    assert (
        document["publication_intent"][
            "publication_id"
        ]
        == document["decision_record"][
            "publication_id"
        ]
    )


def test_serialization_is_canonical_compact_json() -> None:
    serialization = serialize()
    document = json.loads(serialization)

    assert serialization == json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def test_serialization_is_deterministic() -> None:
    evidence = commit_stored_evidence()

    first = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=evidence,
        )
    )
    second = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=evidence,
        )
    )

    assert first == second


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "evidence",
        b"evidence",
        1,
        True,
        (),
    ),
)
def test_invalid_stored_evidence_is_rejected(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="stored_evidence",
    ):
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=value,
        )


def test_serialization_does_not_mutate_source() -> None:
    evidence = commit_stored_evidence()
    before = evidence

    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
        stored_evidence=evidence,
    )

    assert evidence is before


def test_serialization_defines_no_storage_behavior() -> None:
    source = inspect.getsource(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert "sqlite" not in source
    assert "open(" not in source
    assert ".write(" not in source
    assert ".read(" not in source


def test_serialization_defines_no_decision_or_signature_verification() -> None:
    source = inspect.getsource(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert "derive_security_admission" not in source
    assert "verify_security_admission" not in source
