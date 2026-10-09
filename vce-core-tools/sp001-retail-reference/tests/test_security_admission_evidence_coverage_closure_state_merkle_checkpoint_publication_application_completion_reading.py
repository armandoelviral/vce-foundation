import inspect

from dataclasses import replace
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion_reading import (
    read_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion import (
    abort_record,
    commit_record,
    confirmation_set,
    zero_preparation_abort,
)


ApplicationCompletion = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion
)
Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
DecisionRecordStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore
)
Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)
ConfirmationStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore
)
read_completion = (
    read_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion
)


class DecisionStore:
    def __init__(
        self,
        *,
        retained: object,
        events: list[str] | None = None,
    ) -> None:
        self.retained = retained
        self.events = events
        self.read_calls: list[str] = []

    def read(
        self,
        *,
        publication_id: str,
    ) -> object:
        self.read_calls.append(publication_id)
        if self.events is not None:
            self.events.append("decision-read")
        return self.retained

    def create(
        self,
        *,
        decision_record: DecisionRecord,
    ) -> bool:
        raise AssertionError("create must not be called")


class ConfirmationStoreDouble:
    def __init__(
        self,
        *,
        retained: object,
        events: list[str] | None = None,
    ) -> None:
        self.retained = retained
        self.events = events
        self.read_calls: list[str] = []

    def read(
        self,
        *,
        publication_id: str,
    ) -> object:
        self.read_calls.append(publication_id)
        if self.events is not None:
            self.events.append("confirmation-read")
        return self.retained

    def create(
        self,
        *,
        confirmation: Confirmation,
    ) -> bool:
        raise AssertionError("create must not be called")


class IncompleteStore:
    pass


def read(
    *,
    decision_record: object,
    confirmations: object,
    publication_id: str = "publication-001",
) -> ApplicationCompletion | None:
    return read_completion(
        decision_record_store=DecisionStore(
            retained=decision_record,
        ),
        confirmation_store=ConfirmationStoreDouble(
            retained=confirmations,
        ),
        publication_id=publication_id,
    )


def test_reader_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        read_completion,
    )

    assert tuple(signature.parameters) == (
        "decision_record_store",
        "confirmation_store",
        "publication_id",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )

    hints = get_type_hints(read_completion)
    assert hints == {
        "decision_record_store": DecisionRecordStore,
        "confirmation_store": ConfirmationStore,
        "publication_id": str,
        "return": ApplicationCompletion | None,
    }


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        7,
    ),
)
def test_exact_commit_evidence_is_reconstructed(
    size: int,
) -> None:
    decision_record = commit_record(
        size=size,
    )
    confirmations = confirmation_set(
        decision_record,
    )

    result = read(
        decision_record=decision_record,
        confirmations=confirmations,
    )

    assert result == ApplicationCompletion(
        decision_record=decision_record,
        confirmation_set=confirmations,
    )


def test_abort_evidence_is_reconstructed() -> None:
    decision_record = abort_record()
    confirmations = confirmation_set(
        decision_record,
    )

    assert read(
        decision_record=decision_record,
        confirmations=confirmations,
    ) == ApplicationCompletion(
        decision_record=decision_record,
        confirmation_set=confirmations,
    )


def test_zero_preparation_abort_is_complete() -> None:
    decision_record = zero_preparation_abort()
    confirmations = ConfirmationSet(
        confirmations=(),
    )

    assert read(
        decision_record=decision_record,
        confirmations=confirmations,
    ) == ApplicationCompletion(
        decision_record=decision_record,
        confirmation_set=confirmations,
    )


def test_missing_decision_returns_none_without_reading_confirmations() -> None:
    events: list[str] = []
    decision_store = DecisionStore(
        retained=None,
        events=events,
    )
    confirmation_store = ConfirmationStoreDouble(
        retained=object(),
        events=events,
    )

    result = read_completion(
        decision_record_store=decision_store,
        confirmation_store=confirmation_store,
        publication_id="publication-001",
    )

    assert result is None
    assert decision_store.read_calls == [
        "publication-001",
    ]
    assert confirmation_store.read_calls == []
    assert events == [
        "decision-read",
    ]


def test_incomplete_confirmations_return_none() -> None:
    decision_record = commit_record()
    exhaustive = confirmation_set(
        decision_record,
    )
    incomplete = ConfirmationSet(
        confirmations=(
            exhaustive.confirmations[:-1]
        ),
    )

    assert read(
        decision_record=decision_record,
        confirmations=incomplete,
    ) is None


def test_decision_is_read_before_confirmations() -> None:
    events: list[str] = []
    decision_record = commit_record()
    confirmations = confirmation_set(
        decision_record,
    )

    result = read_completion(
        decision_record_store=DecisionStore(
            retained=decision_record,
            events=events,
        ),
        confirmation_store=ConfirmationStoreDouble(
            retained=confirmations,
            events=events,
        ),
        publication_id="publication-001",
    )

    assert isinstance(
        result,
        ApplicationCompletion,
    )
    assert events == [
        "decision-read",
        "confirmation-read",
    ]


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "store",
        1,
        True,
        IncompleteStore(),
    ),
)
def test_decision_record_store_requires_protocol(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="decision_record_store",
    ):
        read_completion(
            decision_record_store=value,
            confirmation_store=ConfirmationStoreDouble(
                retained=ConfirmationSet(
                    confirmations=(),
                ),
            ),
            publication_id="publication-001",
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "store",
        1,
        True,
        IncompleteStore(),
    ),
)
def test_confirmation_store_requires_protocol(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="confirmation_store",
    ):
        read_completion(
            decision_record_store=DecisionStore(
                retained=None,
            ),
            confirmation_store=value,
            publication_id="publication-001",
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        b"publication-001",
        1,
        True,
        [],
        {},
    ),
)
def test_publication_id_requires_exact_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="publication_id must be a string",
    ):
        read_completion(
            decision_record_store=DecisionStore(
                retained=None,
            ),
            confirmation_store=ConfirmationStoreDouble(
                retained=ConfirmationSet(
                    confirmations=(),
                ),
            ),
            publication_id=value,
        )


def test_empty_publication_id_is_rejected_before_reads() -> None:
    decision_store = DecisionStore(
        retained=None,
    )
    confirmation_store = ConfirmationStoreDouble(
        retained=ConfirmationSet(
            confirmations=(),
        ),
    )

    with pytest.raises(
        ValueError,
        match="publication_id must not be empty",
    ):
        read_completion(
            decision_record_store=decision_store,
            confirmation_store=confirmation_store,
            publication_id="",
        )

    assert decision_store.read_calls == []
    assert confirmation_store.read_calls == []


@pytest.mark.parametrize(
    "value",
    (
        object(),
        "decision",
        1,
        True,
        (),
    ),
)
def test_decision_store_read_rejects_invalid_value(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="decision_record_store.read",
    ):
        read(
            decision_record=value,
            confirmations=ConfirmationSet(
                confirmations=(),
            ),
        )


def test_different_retained_publication_id_fails_closed() -> None:
    with pytest.raises(
        ValueError,
        match="different publication_id",
    ):
        read(
            decision_record=commit_record(),
            confirmations=ConfirmationSet(
                confirmations=(),
            ),
            publication_id="different-publication",
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "confirmations",
        1,
        True,
        (),
    ),
)
def test_confirmation_store_read_rejects_invalid_value(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="confirmation_store.read",
    ):
        read(
            decision_record=commit_record(),
            confirmations=value,
        )


def test_contradictory_incomplete_decision_fails_closed() -> None:
    contradictory = replace(
        commit_record(),
        decision=Decision.ABORT,
    )

    with pytest.raises(
        ValueError,
        match="exactly re-derived publication decision",
    ):
        read(
            decision_record=contradictory,
            confirmations=ConfirmationSet(
                confirmations=(),
            ),
        )


def test_reader_defines_no_write_or_participant_effects() -> None:
    source = inspect.getsource(
        read_completion,
    )

    assert ".create(" not in source
    assert ".prepare(" not in source
    assert ".commit(" not in source
    assert ".abort(" not in source
    assert "sqlite" not in source.lower()
    assert "open(" not in source
    assert "subprocess" not in source
    assert "socket" not in source
