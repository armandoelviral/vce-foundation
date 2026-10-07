import inspect

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_deserialization import (
    project_commit,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    create_set,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
StoredEvidence = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence
)


def zero_preparation_abort():
    return (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=create_intent(),
            participant_set=create_set(),
            preparation_set=PreparationSet(
                preparations=(),
            ),
        )
    )


def test_projection_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert tuple(signature.parameters) == (
        "decision_record",
    )
    assert (
        signature.parameters[
            "decision_record"
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
def test_commit_projection_returns_nominal_evidence(
    size: int,
) -> None:
    decision_record, _ = project_commit(
        size=size,
    )

    projected = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=decision_record,
        )
    )

    assert isinstance(
        projected,
        StoredEvidence,
    )
    assert (
        projected.decision_record.decision
        == Decision.COMMIT.value
    )


def test_projection_preserves_exact_signed_intent() -> None:
    decision_record, _ = project_commit()

    projected = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=decision_record,
        )
    )
    expected = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            publication_intent=(
                decision_record.publication_intent
            ),
        )
    )

    assert projected.publication_intent == expected


def test_projection_preserves_exact_decision_record() -> None:
    decision_record, _ = project_commit()

    projected = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=decision_record,
        )
    )
    expected = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record(
            decision_record=decision_record,
        )
    )

    assert projected.decision_record == expected


def test_zero_preparation_abort_retains_signed_intent() -> None:
    decision_record = zero_preparation_abort()

    projected = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=decision_record,
        )
    )

    assert decision_record.decision is Decision.ABORT
    assert (
        projected.decision_record.preparations
        == ()
    )
    assert (
        projected.publication_intent.publication_id
        == decision_record.publication_intent.publication_id
    )
    assert (
        projected.publication_intent.signature
        == (
            decision_record
            .publication_intent
            .checkpoint_signature
            .signature
        )
    )


def test_projection_is_deterministic() -> None:
    decision_record, _ = project_commit()

    first = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=decision_record,
        )
    )
    second = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=decision_record,
        )
    )

    assert first == second
    assert first is not second


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "decision",
        b"decision",
        1,
        True,
        (),
    ),
)
def test_projection_rejects_invalid_decision_record(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="decision_record",
    ):
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=value,
        )


def test_projection_does_not_mutate_source_record() -> None:
    decision_record, _ = project_commit()
    before = decision_record

    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
        decision_record=decision_record,
    )

    assert decision_record is before


def test_projection_defines_no_serialization_or_storage() -> None:
    source = inspect.getsource(
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert "json" not in source
    assert "sqlite" not in source
    assert "open(" not in source
    assert "write" not in source
    assert "read" not in source


def test_projection_defines_no_participant_effects() -> None:
    source = inspect.getsource(
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert ".prepare(" not in source
    assert ".commit(" not in source
    assert ".abort(" not in source
