from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)

UINT64_MAX = (1 << 64) - 1


def create_state(
    *,
    publication_id: str = "publication-001",
    scalar: int = 1,
    phase: Phase = Phase.INTENT_RECORDED,
    revision: int = 1,
) -> PublicationState:
    return PublicationState(
        publication_intent=create_intent(
            publication_id=publication_id,
            scalar=scalar,
        ),
        phase=phase,
        revision=revision,
    )


def test_state_has_exact_fields() -> None:
    assert tuple(
        field.name
        for field in fields(PublicationState)
    ) == (
        "publication_intent",
        "phase",
        "revision",
    )


def test_state_preserves_exact_values() -> None:
    intent = create_intent(
        publication_id="publication-exact",
        scalar=7,
    )

    state = PublicationState(
        publication_intent=intent,
        phase=Phase.PREPARED,
        revision=19,
    )

    assert state.publication_intent is intent
    assert state.phase is Phase.PREPARED
    assert state.revision == 19
    assert type(state.revision) is int


@pytest.mark.parametrize("phase", tuple(Phase))
def test_every_nominal_phase_is_preserved(
    phase: Phase,
) -> None:
    state = create_state(phase=phase)

    assert state.phase is phase


@pytest.mark.parametrize(
    "revision",
    (
        1,
        2,
        7,
        65537,
        UINT64_MAX,
    ),
)
def test_positive_uint64_revisions_are_preserved(
    revision: int,
) -> None:
    state = create_state(revision=revision)

    assert state.revision == revision


@pytest.mark.parametrize("phase", tuple(Phase))
def test_state_does_not_invent_phase_revision_coupling(
    phase: Phase,
) -> None:
    state = create_state(
        phase=phase,
        revision=1,
    )

    assert state.phase is phase
    assert state.revision == 1


@pytest.mark.parametrize(
    "attribute,value",
    (
        ("publication_intent", None),
        ("phase", Phase.COMMITTED),
        ("revision", 2),
    ),
)
def test_state_is_frozen(
    attribute: str,
    value: object,
) -> None:
    state = create_state()

    with pytest.raises(FrozenInstanceError):
        setattr(state, attribute, value)


def test_state_uses_slots() -> None:
    state = create_state()

    assert not hasattr(state, "__dict__")
    assert PublicationState.__slots__ == (
        "publication_intent",
        "phase",
        "revision",
    )


def test_equal_values_are_equal() -> None:
    intent = create_intent(
        publication_id="publication-001",
        scalar=1,
    )

    left = PublicationState(
        publication_intent=intent,
        phase=Phase.INTENT_RECORDED,
        revision=1,
    )
    right = PublicationState(
        publication_intent=intent,
        phase=Phase.INTENT_RECORDED,
        revision=1,
    )

    assert left == right


def test_different_publication_intents_are_not_equal() -> None:
    assert create_state(
        publication_id="publication-001",
    ) != create_state(
        publication_id="publication-002",
    )


def test_different_phases_are_not_equal() -> None:
    assert create_state(
        phase=Phase.PREPARED,
    ) != create_state(
        phase=Phase.COMMIT_DECIDED,
    )


def test_different_revisions_are_not_equal() -> None:
    assert create_state(revision=1) != create_state(revision=2)


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "publication-intent",
        1,
        (),
    ),
)
def test_publication_intent_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "publication_intent must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationIntent"
        ),
    ):
        PublicationState(
            publication_intent=value,
            phase=Phase.INTENT_RECORDED,
            revision=1,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "INTENT_RECORDED",
        1,
        (),
    ),
)
def test_phase_rejects_invalid_nominal_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "phase must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationPhase"
        ),
    ):
        PublicationState(
            publication_intent=create_intent(
                publication_id="publication-001",
                scalar=1,
            ),
            phase=value,
            revision=1,
        )


@pytest.mark.parametrize(
    "value",
    (
        0,
        -1,
        -(1 << 64),
    ),
)
def test_revision_rejects_non_positive_values(
    value: int,
) -> None:
    with pytest.raises(ValueError, match="revision"):
        create_state(revision=value)


def test_revision_rejects_uint64_overflow() -> None:
    with pytest.raises(ValueError, match="revision"):
        create_state(revision=UINT64_MAX + 1)


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        False,
        1.0,
        "1",
        b"1",
        (),
    ),
)
def test_revision_requires_exact_integer_type(
    value: object,
) -> None:
    with pytest.raises(TypeError, match="revision"):
        create_state(revision=value)


def test_state_defines_representation_only() -> None:
    public_names = {
        name
        for name in vars(PublicationState)
        if not name.startswith("_")
    }

    assert public_names == {
        "publication_intent",
        "phase",
        "revision",
    }


@pytest.mark.parametrize(
    "forbidden_term",
    (
        "persist",
        "prepare",
        "commit",
        "abort",
        "rollback",
        "transition",
        "compare_and_swap",
        "lock",
        "wal",
    ),
)
def test_state_defines_no_transaction_behavior(
    forbidden_term: str,
) -> None:
    public_names = tuple(
        name.lower()
        for name in vars(PublicationState)
        if not name.startswith("_")
    )

    assert not any(
        forbidden_term in name
        for name in public_names
    )


def test_state_contains_no_local_clock_or_timestamp() -> None:
    field_names = {
        field.name
        for field in fields(PublicationState)
    }

    assert field_names.isdisjoint(
        {
            "created_at",
            "updated_at",
            "recorded_at",
            "timestamp",
        }
    )
