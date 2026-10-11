from pathlib import Path

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion_reading import (
    read_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_sqlite_decision_evidence_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_sqlite_participant_application_confirmation_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteParticipantApplicationConfirmationStore,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion import (
    abort_record,
    commit_record,
    confirmation_set,
    zero_preparation_abort,
)


@pytest.mark.parametrize(
    "record_factory",
    (commit_record, abort_record, zero_preparation_abort),
    ids=("commit", "abort", "zero-preparation-abort"),
)
def test_completion_is_reconstructed_after_sqlite_stores_reopen(
    tmp_path: Path,
    record_factory,
) -> None:
    decision_record = record_factory()
    confirmations = confirmation_set(decision_record)
    publication_id = (
        decision_record.publication_intent.publication_id
    )

    decision_database = tmp_path / "decisions.sqlite3"
    confirmation_database = tmp_path / "confirmations.sqlite3"

    first_decision_store = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
            database_path=decision_database,
            participant_set=decision_record.participant_set,
        )
    )
    first_confirmation_store = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteParticipantApplicationConfirmationStore(
            database_path=confirmation_database,
        )
    )

    assert first_decision_store.create(
        decision_record=decision_record,
    )
    for confirmation in confirmations.confirmations:
        assert first_confirmation_store.create(
            confirmation=confirmation,
        )

    reopened_decision_store = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
            database_path=decision_database,
            participant_set=decision_record.participant_set,
        )
    )
    reopened_confirmation_store = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteParticipantApplicationConfirmationStore(
            database_path=confirmation_database,
        )
    )

    result = (
        read_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion(
            decision_record_store=reopened_decision_store,
            confirmation_store=reopened_confirmation_store,
            publication_id=publication_id,
        )
    )

    assert result == (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion(
            decision_record=decision_record,
            confirmation_set=confirmations,
        )
    )
