from dataclasses import FrozenInstanceError, replace
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    create_state,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
Preparation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)


def prepared_state(
    *,
    publication_id: str = "publication-001",
    revision: int = 2,
):
    return create_state(
        publication_id=publication_id,
        phase=Phase.PREPARED,
        revision=revision,
    )


def preparation(
    participant_id: str,
    *,
    state=None,
):
    if state is None:
        state = prepared_state()

    return Preparation(
        participant_id=participant_id,
        publication_state=state,
    )


def create_set(
    size: int = 3,
):
    state = prepared_state()

    return PreparationSet(
        preparations=tuple(
            preparation(
                f"participant-{index:03d}",
                state=state,
            )
            for index in range(1, size + 1)
        ),
    )


def test_preparation_set_has_exact_field() -> None:
    hints = get_type_hints(PreparationSet)

    assert tuple(hints) == (
        "preparations",
    )
    assert hints["preparations"] == tuple[
        Preparation,
        ...,
    ]


def test_preparation_set_preserves_exact_tuple() -> None:
    state = prepared_state()
    preparations = (
        preparation(
            "participant-001",
            state=state,
        ),
        preparation(
            "participant-002",
            state=state,
        ),
    )

    preparation_set = PreparationSet(
        preparations=preparations,
    )

    assert (
        preparation_set.preparations
        is preparations
    )


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
def test_canonical_sets_are_accepted(
    size: int,
) -> None:
    preparation_set = create_set(size)

    assert tuple(
        value.participant_id
        for value
        in preparation_set.preparations
    ) == tuple(
        f"participant-{index:03d}"
        for index in range(1, size + 1)
    )


def test_preparation_set_is_frozen() -> None:
    preparation_set = create_set()

    with pytest.raises(FrozenInstanceError):
        preparation_set.preparations = ()


def test_preparation_set_uses_slots() -> None:
    preparation_set = create_set()

    assert not hasattr(
        preparation_set,
        "__dict__",
    )


def test_equal_values_are_equal() -> None:
    state = prepared_state()
    preparations = (
        preparation(
            "participant-001",
            state=state,
        ),
    )

    assert (
        PreparationSet(
            preparations=preparations,
        )
        ==
        PreparationSet(
            preparations=preparations,
        )
    )


def test_different_sets_are_not_equal() -> None:
    state = prepared_state()

    assert (
        PreparationSet(
            preparations=(
                preparation(
                    "participant-001",
                    state=state,
                ),
            ),
        )
        !=
        PreparationSet(
            preparations=(
                preparation(
                    "participant-001",
                    state=state,
                ),
                preparation(
                    "participant-002",
                    state=state,
                ),
            ),
        )
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        [],
        {},
        set(),
        "preparations",
        b"preparations",
        1,
        True,
    ),
)
def test_preparations_requires_tuple(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="preparations must be a tuple",
    ):
        PreparationSet(
            preparations=value,
        )


def test_empty_set_is_preserved() -> None:
    preparation_set = PreparationSet(
        preparations=(),
    )

    assert preparation_set.preparations == ()


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "preparation",
        b"preparation",
        1,
        True,
        (),
        [],
    ),
)
def test_elements_require_nominal_preparation(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="preparations must contain only",
    ):
        PreparationSet(
            preparations=(value,),
        )


def test_duplicate_participant_identifiers_are_rejected() -> None:
    state = prepared_state()

    with pytest.raises(
        ValueError,
        match="unique participant identifiers",
    ):
        PreparationSet(
            preparations=(
                preparation(
                    "participant-001",
                    state=state,
                ),
                preparation(
                    "participant-001",
                    state=state,
                ),
            ),
        )


def test_duplicate_identifier_is_rejected_across_distinct_states() -> None:
    state = prepared_state()
    later_state = replace(
        state,
        revision=3,
    )

    with pytest.raises(
        ValueError,
        match="unique participant identifiers",
    ):
        PreparationSet(
            preparations=(
                preparation(
                    "participant-001",
                    state=state,
                ),
                preparation(
                    "participant-001",
                    state=later_state,
                ),
            ),
        )


def test_noncanonical_participant_order_is_rejected() -> None:
    state = prepared_state()

    with pytest.raises(
        ValueError,
        match="canonical participant identifier order",
    ):
        PreparationSet(
            preparations=(
                preparation(
                    "participant-002",
                    state=state,
                ),
                preparation(
                    "participant-001",
                    state=state,
                ),
            ),
        )


def test_input_is_not_reordered() -> None:
    state = prepared_state()
    preparations = (
        preparation(
            "participant-002",
            state=state,
        ),
        preparation(
            "participant-001",
            state=state,
        ),
    )

    with pytest.raises(ValueError):
        PreparationSet(
            preparations=preparations,
        )

    assert tuple(
        value.participant_id
        for value in preparations
    ) == (
        "participant-002",
        "participant-001",
    )


def test_lexical_case_sensitive_order_is_accepted() -> None:
    state = prepared_state()
    preparation_set = PreparationSet(
        preparations=(
            preparation(
                "A",
                state=state,
            ),
            preparation(
                "a",
                state=state,
            ),
        ),
    )

    assert tuple(
        value.participant_id
        for value
        in preparation_set.preparations
    ) == (
        "A",
        "a",
    )


def test_different_publication_identifiers_are_rejected() -> None:
    first = prepared_state(
        publication_id="publication-001",
    )
    second = prepared_state(
        publication_id="publication-002",
    )

    with pytest.raises(
        ValueError,
        match="exact same publication intent",
    ):
        PreparationSet(
            preparations=(
                preparation(
                    "participant-001",
                    state=first,
                ),
                preparation(
                    "participant-002",
                    state=second,
                ),
            ),
        )


def test_different_signed_intents_with_same_identifier_are_rejected() -> None:
    first = prepared_state(
        publication_id="publication-001",
    )
    second = prepared_state(
        publication_id="publication-001",
    )

    assert (
        first.publication_intent
        != second.publication_intent
    )

    with pytest.raises(
        ValueError,
        match="exact same publication intent",
    ):
        PreparationSet(
            preparations=(
                preparation(
                    "participant-001",
                    state=first,
                ),
                preparation(
                    "participant-002",
                    state=second,
                ),
            ),
        )


def test_same_intent_with_different_revisions_is_accepted() -> None:
    first = prepared_state(
        revision=2,
    )
    second = replace(
        first,
        revision=7,
    )

    preparation_set = PreparationSet(
        preparations=(
            preparation(
                "participant-001",
                state=first,
            ),
            preparation(
                "participant-002",
                state=second,
            ),
        ),
    )

    assert tuple(
        value.publication_state.revision
        for value
        in preparation_set.preparations
    ) == (
        2,
        7,
    )


def test_exact_shared_intent_reference_is_preserved() -> None:
    state = prepared_state()
    preparation_set = PreparationSet(
        preparations=(
            preparation(
                "participant-001",
                state=state,
            ),
            preparation(
                "participant-002",
                state=state,
            ),
        ),
    )

    first_intent = (
        preparation_set
        .preparations[0]
        .publication_state
        .publication_intent
    )
    second_intent = (
        preparation_set
        .preparations[1]
        .publication_state
        .publication_intent
    )

    assert first_intent is second_intent


def test_set_defines_validation_only() -> None:
    import inspect

    source = inspect.getsource(
        PreparationSet
    ).lower()

    for forbidden in (
        "prepare(",
        "commit(",
        "abort(",
        "coordinator",
        "quorum",
        "retry",
        "timeout",
        "sqlite",
        "socket",
        "http",
        "private_key",
    ):
        assert forbidden not in source


def test_set_imports_no_unsafe_capability() -> None:
    import inspect

    from sp001.services import (
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set,
    )

    source = inspect.getsource(
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set
    )

    assert "pickle" not in source
    assert "eval(" not in source
    assert "exec(" not in source
