import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    terminal_state,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
StoredConfirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation
)


def stored_state(
    *,
    phase: Phase = Phase.COMMITTED,
    revision: int = 4,
    scalar: int = 1,
):
    return (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state(
            state=terminal_state(
                phase=phase,
                revision=revision,
                scalar=scalar,
            ),
        )
    )


def stored_confirmation(
    *,
    participant_id: str = "participant-001",
    decision: Decision = Decision.COMMIT,
    state=None,
) -> StoredConfirmation:
    if state is None:
        phase = (
            Phase.COMMITTED
            if decision is Decision.COMMIT
            else Phase.ABORTED
        )
        state = stored_state(
            phase=phase,
        )

    return StoredConfirmation(
        storage_schema_version=1,
        participant_id=participant_id,
        decision=decision.value,
        publication_state=state,
    )


def test_stored_confirmation_has_exact_fields() -> None:
    assert tuple(
        field.name
        for field in fields(StoredConfirmation)
    ) == (
        "storage_schema_version",
        "participant_id",
        "decision",
        "publication_state",
    )


def test_stored_confirmation_preserves_exact_values() -> None:
    state = stored_state()

    value = StoredConfirmation(
        storage_schema_version=1,
        participant_id="participant-017",
        decision="COMMIT",
        publication_state=state,
    )

    assert value.storage_schema_version == 1
    assert value.participant_id == "participant-017"
    assert value.decision == "COMMIT"
    assert value.publication_state is state


def test_stored_confirmation_is_frozen() -> None:
    value = stored_confirmation()

    with pytest.raises(FrozenInstanceError):
        value.participant_id = "participant-002"


def test_stored_confirmation_uses_slots() -> None:
    value = stored_confirmation()

    assert not hasattr(value, "__dict__")
    assert StoredConfirmation.__slots__ == (
        "storage_schema_version",
        "participant_id",
        "decision",
        "publication_state",
    )


def test_equal_primitive_graphs_are_equal() -> None:
    state = stored_state()

    assert (
        stored_confirmation(
            state=state,
        )
        == stored_confirmation(
            state=state,
        )
    )


def test_different_participant_identifiers_are_not_equal() -> None:
    state = stored_state()

    assert (
        stored_confirmation(
            participant_id="participant-001",
            state=state,
        )
        != stored_confirmation(
            participant_id="participant-002",
            state=state,
        )
    )


def test_different_decisions_are_not_equal() -> None:
    assert (
        stored_confirmation(
            decision=Decision.COMMIT,
        )
        != stored_confirmation(
            decision=Decision.ABORT,
        )
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        1.0,
        "1",
        b"1",
        object(),
    ),
)
def test_storage_schema_version_requires_exact_integer(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="storage_schema_version must be an integer",
    ):
        StoredConfirmation(
            storage_schema_version=value,
            participant_id="participant-001",
            decision="COMMIT",
            publication_state=stored_state(),
        )


@pytest.mark.parametrize(
    "value",
    (
        0,
        -1,
        -(2**63),
        2**64,
    ),
)
def test_storage_schema_version_requires_positive_uint64(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="storage_schema_version",
    ):
        StoredConfirmation(
            storage_schema_version=value,
            participant_id="participant-001",
            decision="COMMIT",
            publication_state=stored_state(),
        )


@pytest.mark.parametrize(
    "value",
    (
        2,
        3,
        2**32,
        2**64 - 1,
    ),
)
def test_unknown_storage_schema_version_fails_closed(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="unsupported storage schema version",
    ):
        StoredConfirmation(
            storage_schema_version=value,
            participant_id="participant-001",
            decision="COMMIT",
            publication_state=stored_state(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        1,
        b"participant-001",
        object(),
    ),
)
def test_participant_identifier_requires_exact_string(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="participant_id must be a string",
    ):
        StoredConfirmation(
            storage_schema_version=1,
            participant_id=value,
            decision="COMMIT",
            publication_state=stored_state(),
        )


def test_empty_participant_identifier_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="participant_id must not be empty",
    ):
        StoredConfirmation(
            storage_schema_version=1,
            participant_id="",
            decision="COMMIT",
            publication_state=stored_state(),
        )


@pytest.mark.parametrize(
    "value",
    (
        " ",
        "\t",
        "participant/opaque",
        "PARTICIPANT-001",
    ),
)
def test_opaque_nonempty_participant_identifier_is_preserved(
    value: str,
) -> None:
    assert (
        stored_confirmation(
            participant_id=value,
        ).participant_id
        == value
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        1,
        b"COMMIT",
        Decision.COMMIT,
        object(),
    ),
)
def test_decision_requires_exact_string(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="decision must be a string",
    ):
        StoredConfirmation(
            storage_schema_version=1,
            participant_id="participant-001",
            decision=value,
            publication_state=stored_state(),
        )


@pytest.mark.parametrize(
    "value",
    (
        "",
        "commit",
        "abort",
        "PREPARED",
        "UNKNOWN",
        " COMMIT",
        "COMMIT ",
    ),
)
def test_decision_rejects_unsupported_value(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="supported publication decision",
    ):
        StoredConfirmation(
            storage_schema_version=1,
            participant_id="participant-001",
            decision=value,
            publication_state=stored_state(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        1,
        "state",
        object(),
    ),
)
def test_publication_state_requires_nominal_stored_type(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="publication_state must be a",
    ):
        StoredConfirmation(
            storage_schema_version=1,
            participant_id="participant-001",
            decision="COMMIT",
            publication_state=value,
        )


@pytest.mark.parametrize(
    ("decision", "phase"),
    (
        (
            Decision.COMMIT,
            Phase.COMMITTED,
        ),
        (
            Decision.ABORT,
            Phase.ABORTED,
        ),
    ),
)
def test_matching_terminal_decision_is_preserved(
    decision: Decision,
    phase: Phase,
) -> None:
    state = stored_state(
        phase=phase,
    )

    value = stored_confirmation(
        decision=decision,
        state=state,
    )

    assert value.decision == decision.value
    assert value.publication_state.phase == phase.value


@pytest.mark.parametrize(
    ("decision", "phase"),
    tuple(
        (
            decision,
            phase,
        )
        for decision in Decision
        for phase in Phase
        if (
            decision,
            phase,
        )
        not in (
            (
                Decision.COMMIT,
                Phase.COMMITTED,
            ),
            (
                Decision.ABORT,
                Phase.ABORTED,
            ),
        )
    ),
)
def test_nonmatching_phase_is_rejected(
    decision: Decision,
    phase: Phase,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "publication_state phase must confirm "
            "the stored publication decision"
        ),
    ):
        stored_confirmation(
            decision=decision,
            state=stored_state(
                phase=phase,
            ),
        )


def test_publication_identifier_is_retained_once_in_state() -> None:
    value = stored_confirmation()

    assert (
        value.publication_state.publication_id
        == "publication-001"
    )
    assert not hasattr(value, "publication_id")


def test_complete_signed_state_is_preserved() -> None:
    state = stored_state(
        scalar=2,
    )

    value = stored_confirmation(
        state=state,
    )

    assert value.publication_state is state
    assert value.publication_state.signature
    assert value.publication_state.checkpoint_serialization


def test_portable_record_preserves_revision() -> None:
    state = stored_state(
        revision=2**64 - 1,
    )

    value = stored_confirmation(
        state=state,
    )

    assert value.publication_state.revision == 2**64 - 1


def test_record_defines_no_serialization_behavior() -> None:
    members = set(StoredConfirmation.__dict__)

    assert members.isdisjoint(
        {
            "serialize",
            "deserialize",
            "parse",
            "to_json",
            "from_json",
        }
    )


def test_record_defines_no_storage_or_effect_behavior() -> None:
    members = set(StoredConfirmation.__dict__)

    assert members.isdisjoint(
        {
            "create",
            "read",
            "write",
            "prepare",
            "commit",
            "abort",
            "apply",
        }
    )


def test_record_imports_no_unsafe_capability() -> None:
    module = inspect.getmodule(StoredConfirmation)
    assert module is not None

    source = inspect.getsource(module)

    assert "sqlite" not in source.lower()
    assert "subprocess" not in source
    assert "socket" not in source
    assert "eval(" not in source
    assert "exec(" not in source
    assert "__import__" not in source
