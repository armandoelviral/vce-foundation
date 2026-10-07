import inspect
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_projection import (
    create_decision_record,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    create_set as create_participant_set,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
StoredDecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)
deserialize = (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record
)
project = (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record
)


def project_commit(
    *,
    size: int = 3,
):
    decision_record = create_decision_record(
        size=size,
        decision=Decision.COMMIT,
    )
    stored_record = project(
        decision_record=decision_record,
    )

    return decision_record, stored_record


def project_abort_with_incomplete_preparations():
    complete = create_decision_record(
        size=3,
        decision=Decision.ABORT,
    )
    incomplete_set = PreparationSet(
        preparations=(
            complete
            .preparation_set
            .preparations[:2]
        ),
    )
    incomplete = replace(
        complete,
        preparation_set=incomplete_set,
    )

    return incomplete, project(
        decision_record=incomplete,
    )


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        5,
    ),
)
def test_commit_round_trip_is_exact(
    size: int,
) -> None:
    original, stored = project_commit(
        size=size,
    )

    rebuilt = deserialize(
        stored_record=stored,
        participant_set=original.participant_set,
    )

    assert rebuilt == original
    assert rebuilt.decision is Decision.COMMIT


def test_abort_with_incomplete_evidence_round_trips() -> None:
    original, stored = (
        project_abort_with_incomplete_preparations()
    )

    rebuilt = deserialize(
        stored_record=stored,
        participant_set=original.participant_set,
    )

    assert rebuilt == original
    assert rebuilt.decision is Decision.ABORT


def test_rebuilt_record_uses_exact_provisioned_participant_set() -> None:
    _, stored = project_commit()
    provisioned = create_participant_set(
        size=3,
    )

    rebuilt = deserialize(
        stored_record=stored,
        participant_set=provisioned,
    )

    assert rebuilt.participant_set is provisioned


def test_stored_commit_without_exhaustive_evidence_fails_closed() -> None:
    original, stored_abort = (
        project_abort_with_incomplete_preparations()
    )
    tampered = replace(
        stored_abort,
        decision="COMMIT",
    )

    with pytest.raises(
        ValueError,
        match="re-derived decision",
    ):
        deserialize(
            stored_record=tampered,
            participant_set=original.participant_set,
        )


def test_stored_abort_with_commit_evidence_fails_closed() -> None:
    original, stored_commit = project_commit()
    tampered = replace(
        stored_commit,
        decision="ABORT",
    )

    with pytest.raises(
        ValueError,
        match="re-derived decision",
    ):
        deserialize(
            stored_record=tampered,
            participant_set=original.participant_set,
        )


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        4,
        5,
    ),
)
def test_different_provisioned_roster_is_rejected(
    size: int,
) -> None:
    _, stored = project_commit(
        size=3,
    )

    with pytest.raises(
        ValueError,
        match="provisioned participant set",
    ):
        deserialize(
            stored_record=stored,
            participant_set=create_participant_set(
                size=size,
            ),
        )


def test_changed_stored_participant_id_is_rejected() -> None:
    original, stored = project_commit()
    changed = replace(
        stored,
        participant_ids=(
            "participant-000",
            *stored.participant_ids[:2],
        ),
    )

    with pytest.raises(
        ValueError,
        match="provisioned participant set",
    ):
        deserialize(
            stored_record=changed,
            participant_set=original.participant_set,
        )


@pytest.mark.parametrize(
    "version",
    (
        2,
        7,
        (1 << 64) - 1,
    ),
)
def test_unsupported_storage_schema_version_is_rejected(
    version: int,
) -> None:
    original, stored = project_commit()
    changed = replace(
        stored,
        storage_schema_version=version,
    )

    with pytest.raises(
        ValueError,
        match="unsupported",
    ):
        deserialize(
            stored_record=changed,
            participant_set=original.participant_set,
        )


def test_conflicting_preparation_intent_is_rejected() -> None:
    original, stored = project_commit()
    other, other_stored = project_commit()
    other_state = other_stored.preparations[0][1]
    changed = replace(
        stored,
        preparations=(
            stored.preparations[0],
            (
                stored.preparations[1][0],
                other_state,
            ),
            stored.preparations[2],
        ),
    )

    with pytest.raises(
        ValueError,
        match="exact same publication intent",
    ):
        deserialize(
            stored_record=changed,
            participant_set=original.participant_set,
        )

    assert other is not original


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "stored-record",
        1,
        True,
        (),
    ),
)
def test_stored_record_rejects_invalid_type(
    value: object,
) -> None:
    participant_set = create_participant_set()

    with pytest.raises(
        TypeError,
        match="stored_record",
    ):
        deserialize(
            stored_record=value,
            participant_set=participant_set,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "participant-set",
        1,
        True,
        (),
    ),
)
def test_participant_set_rejects_invalid_type(
    value: object,
) -> None:
    _, stored = project_commit()

    with pytest.raises(
        TypeError,
        match="participant_set",
    ):
        deserialize(
            stored_record=stored,
            participant_set=value,
        )


def test_deserialization_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        deserialize
    )

    assert tuple(signature.parameters) == (
        "stored_record",
        "participant_set",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )
    assert (
        signature.parameters[
            "stored_record"
        ].annotation
        is StoredDecisionRecord
    )
    assert (
        signature.parameters[
            "participant_set"
        ].annotation
        is ParticipantSet
    )
    assert signature.return_annotation is DecisionRecord


def test_deserialization_defines_no_storage_or_participant_effects() -> None:
    source = inspect.getsource(
        deserialize
    ).lower()

    for forbidden in (
        "sqlite",
        "database",
        "compare_and_swap",
        ".prepare(",
        ".commit(",
        ".abort(",
        "network",
        "http",
        "socket",
    ):
        assert forbidden not in source
