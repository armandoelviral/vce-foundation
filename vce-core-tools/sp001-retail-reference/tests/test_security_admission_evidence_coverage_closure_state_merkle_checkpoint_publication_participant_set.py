from dataclasses import FrozenInstanceError
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
)


class Participant:
    def __init__(
        self,
        participant_id,
    ) -> None:
        self._participant_id = participant_id

    @property
    def participant_id(self):
        return self._participant_id

    def prepare(
        self,
        *,
        publication_intent,
    ):
        raise NotImplementedError

    def commit(
        self,
        *,
        publication_id,
    ):
        raise NotImplementedError

    def abort(
        self,
        *,
        publication_id,
    ):
        raise NotImplementedError


class IncompleteParticipant:
    participant_id = "participant-001"


def participant(
    index: int,
) -> Participant:
    return Participant(
        f"participant-{index:03d}"
    )


def create_set(
    size: int = 3,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet:
    return SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
        participants=tuple(
            participant(index)
            for index in range(1, size + 1)
        ),
    )


def test_participant_set_has_exact_field() -> None:
    hints = get_type_hints(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
    )

    assert tuple(hints) == (
        "participants",
    )
    assert hints["participants"] == tuple[
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant,
        ...,
    ]


def test_participant_set_preserves_exact_tuple() -> None:
    participants = (
        participant(1),
        participant(2),
        participant(3),
    )

    participant_set = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=participants,
        )
    )

    assert participant_set.participants is participants


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        5,
        10,
    ),
)
def test_canonical_participant_sets_are_accepted(
    size: int,
) -> None:
    participant_set = create_set(size)

    assert tuple(
        value.participant_id
        for value in participant_set.participants
    ) == tuple(
        f"participant-{index:03d}"
        for index in range(1, size + 1)
    )


def test_participant_set_is_frozen() -> None:
    participant_set = create_set()

    with pytest.raises(FrozenInstanceError):
        participant_set.participants = ()


def test_participant_set_uses_slots() -> None:
    participant_set = create_set()

    assert not hasattr(
        participant_set,
        "__dict__",
    )


def test_same_participant_references_are_equal() -> None:
    participants = (
        participant(1),
        participant(2),
    )

    assert (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=participants,
        )
        ==
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=participants,
        )
    )


def test_different_participant_tuples_are_not_equal() -> None:
    assert create_set(2) != create_set(3)


@pytest.mark.parametrize(
    "value",
    (
        None,
        [],
        {},
        set(),
        "participants",
        b"participants",
        1,
        True,
    ),
)
def test_participants_requires_tuple(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="participants must be a tuple",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=value,
        )


def test_empty_participant_set_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "participant",
        b"participant",
        1,
        True,
        (),
        IncompleteParticipant(),
    ),
)
def test_elements_must_implement_participant_protocol(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="participants must contain only",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=(value,),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        b"participant-001",
        1,
        True,
        (),
    ),
)
def test_participant_identifier_requires_exact_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="participant_id must be a string",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=(
                Participant(value),
            ),
        )


@pytest.mark.parametrize(
    "value",
    (
        "",
        " ",
        "\t",
        "\n",
        "  \t\n  ",
    ),
)
def test_blank_participant_identifier_is_rejected(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="participant_id must not be blank",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=(
                Participant(value),
            ),
        )


@pytest.mark.parametrize(
    "value",
    (
        "participant-001",
        "node://region-a/001",
        "urn:sp001:participant:alpha",
        "AWS/us-east-1/primary",
        "participante-á",
    ),
)
def test_opaque_nonblank_identifiers_are_preserved(
    value: str,
) -> None:
    instance = Participant(value)
    participant_set = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=(instance,),
        )
    )

    assert (
        participant_set.participants[0].participant_id
        == value
    )


def test_duplicate_participant_identifiers_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="unique participant identifiers",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=(
                Participant("participant-001"),
                Participant("participant-001"),
            ),
        )


def test_duplicate_identifier_is_rejected_for_distinct_objects() -> None:
    first = Participant("participant-001")
    second = Participant("participant-001")

    assert first is not second

    with pytest.raises(
        ValueError,
        match="unique participant identifiers",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=(
                first,
                second,
            ),
        )


def test_noncanonical_participant_order_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="canonical participant identifier order",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=(
                participant(2),
                participant(1),
            ),
        )


def test_sorting_is_lexical_and_case_sensitive() -> None:
    participant_set = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=(
                Participant("A"),
                Participant("a"),
            ),
        )
    )

    assert tuple(
        value.participant_id
        for value in participant_set.participants
    ) == (
        "A",
        "a",
    )


def test_participant_set_does_not_reorder_input() -> None:
    participants = (
        participant(2),
        participant(1),
    )

    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet(
            participants=participants,
        )

    assert tuple(
        value.participant_id
        for value in participants
    ) == (
        "participant-002",
        "participant-001",
    )


def test_participant_set_defines_validation_only() -> None:
    import inspect

    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
    ).lower()

    assert "prepare(" not in source
    assert "commit(" not in source
    assert "abort(" not in source
    assert "coordinator" not in source
    assert "quorum" not in source
    assert "retry" not in source
    assert "timeout" not in source


def test_participant_set_imports_no_external_capability() -> None:
    import inspect

    from sp001.services import (
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set,
    )

    source = inspect.getsource(
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set
    ).lower()

    for forbidden in (
        "sqlite",
        "socket",
        "http",
        "grpc",
        "requests",
        "private_key",
        "pickle",
        "eval(",
        "exec(",
    ):
        assert forbidden not in source
