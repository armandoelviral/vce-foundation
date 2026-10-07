import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_deserialization import (
    project_commit,
)


StoredEvidence = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence
)


def create_stored_evidence(
    *,
    size: int = 3,
) -> StoredEvidence:
    decision_record, stored_record = project_commit(
        size=size,
    )
    stored_intent = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            publication_intent=(
                decision_record.publication_intent
            ),
        )
    )

    return StoredEvidence(
        publication_intent=stored_intent,
        decision_record=stored_record,
    )


def test_stored_evidence_has_exact_fields() -> None:
    assert tuple(
        field.name
        for field in fields(StoredEvidence)
    ) == (
        "publication_intent",
        "decision_record",
    )


def test_stored_evidence_preserves_exact_values() -> None:
    decision_record, stored_record = project_commit()
    stored_intent = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            publication_intent=(
                decision_record.publication_intent
            ),
        )
    )

    evidence = StoredEvidence(
        publication_intent=stored_intent,
        decision_record=stored_record,
    )

    assert evidence.publication_intent is stored_intent
    assert evidence.decision_record is stored_record


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
def test_every_participant_cardinality_is_preserved(
    size: int,
) -> None:
    evidence = create_stored_evidence(
        size=size,
    )

    assert len(
        evidence.decision_record.participant_ids
    ) == size
    assert len(
        evidence.decision_record.preparations
    ) == size


def test_equal_values_are_equal() -> None:
    decision_record, stored_record = project_commit()
    stored_intent = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            publication_intent=(
                decision_record.publication_intent
            ),
        )
    )

    assert StoredEvidence(
        publication_intent=stored_intent,
        decision_record=stored_record,
    ) == StoredEvidence(
        publication_intent=stored_intent,
        decision_record=stored_record,
    )


def test_stored_evidence_is_frozen() -> None:
    evidence = create_stored_evidence()

    with pytest.raises(FrozenInstanceError):
        evidence.publication_intent = (
            evidence.publication_intent
        )


def test_stored_evidence_uses_slots() -> None:
    evidence = create_stored_evidence()

    assert not hasattr(evidence, "__dict__")


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "intent",
        b"intent",
        1,
        True,
        (),
    ),
)
def test_publication_intent_rejects_invalid_type(
    value: object,
) -> None:
    evidence = create_stored_evidence()

    with pytest.raises(
        TypeError,
        match="publication_intent",
    ):
        StoredEvidence(
            publication_intent=value,
            decision_record=evidence.decision_record,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "record",
        b"record",
        1,
        True,
        (),
    ),
)
def test_decision_record_rejects_invalid_type(
    value: object,
) -> None:
    evidence = create_stored_evidence()

    with pytest.raises(
        TypeError,
        match="decision_record",
    ):
        StoredEvidence(
            publication_intent=(
                evidence.publication_intent
            ),
            decision_record=value,
        )


def test_different_publication_identifiers_are_rejected() -> None:
    evidence = create_stored_evidence()
    changed_intent = replace(
        evidence.publication_intent,
        publication_id="different-publication",
    )

    with pytest.raises(
        ValueError,
        match="same publication_id",
    ):
        StoredEvidence(
            publication_intent=changed_intent,
            decision_record=evidence.decision_record,
        )


def test_constructor_has_exact_api() -> None:
    signature = inspect.signature(StoredEvidence)

    assert tuple(signature.parameters) == (
        "publication_intent",
        "decision_record",
    )
    assert (
        signature.parameters[
            "publication_intent"
        ].annotation
        is not inspect.Parameter.empty
    )
    assert (
        signature.parameters[
            "decision_record"
        ].annotation
        is not inspect.Parameter.empty
    )


def test_value_defines_no_serialization_behavior() -> None:
    public_members = {
        name
        for name in StoredEvidence.__dict__
        if not name.startswith("_")
    }

    assert "serialize" not in public_members
    assert "deserialize" not in public_members
    assert "parse" not in public_members


def test_value_defines_no_storage_behavior() -> None:
    public_members = {
        name
        for name in StoredEvidence.__dict__
        if not name.startswith("_")
    }

    assert public_members.isdisjoint(
        {
            "read",
            "create",
            "write",
            "save",
            "compare_and_swap",
        }
    )


def test_value_defines_no_decision_derivation() -> None:
    public_members = {
        name
        for name in StoredEvidence.__dict__
        if not name.startswith("_")
    }

    assert public_members.isdisjoint(
        {
            "derive",
            "prepare",
            "commit",
            "abort",
        }
    )
