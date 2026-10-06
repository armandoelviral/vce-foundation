from dataclasses import FrozenInstanceError
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
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


def prepared_state():
    return create_state(
        phase=Phase.PREPARED,
        revision=2,
    )


def create_preparation(
    *,
    participant_id: str = "participant-001",
):
    return Preparation(
        participant_id=participant_id,
        publication_state=prepared_state(),
    )


def test_preparation_has_exact_fields() -> None:
    hints = get_type_hints(Preparation)

    assert tuple(hints) == (
        "participant_id",
        "publication_state",
    )
    assert hints == {
        "participant_id": str,
        "publication_state": (
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
        ),
    }


def test_preparation_preserves_exact_values() -> None:
    state = prepared_state()
    preparation = Preparation(
        participant_id="node://region-a/001",
        publication_state=state,
    )

    assert (
        preparation.participant_id
        == "node://region-a/001"
    )
    assert preparation.publication_state is state


def test_preparation_is_frozen() -> None:
    preparation = create_preparation()

    with pytest.raises(FrozenInstanceError):
        preparation.participant_id = (
            "participant-002"
        )


def test_preparation_uses_slots() -> None:
    preparation = create_preparation()

    assert not hasattr(
        preparation,
        "__dict__",
    )


def test_equal_values_are_equal() -> None:
    state = prepared_state()

    assert (
        Preparation(
            participant_id="participant-001",
            publication_state=state,
        )
        ==
        Preparation(
            participant_id="participant-001",
            publication_state=state,
        )
    )


def test_different_participant_identifiers_are_not_equal() -> None:
    state = prepared_state()

    assert (
        Preparation(
            participant_id="participant-001",
            publication_state=state,
        )
        !=
        Preparation(
            participant_id="participant-002",
            publication_state=state,
        )
    )


def test_different_prepared_states_are_not_equal() -> None:
    first = prepared_state()
    second = create_state(
        publication_id="publication-002",
        phase=Phase.PREPARED,
        revision=2,
    )

    assert (
        Preparation(
            participant_id="participant-001",
            publication_state=first,
        )
        !=
        Preparation(
            participant_id="participant-001",
            publication_state=second,
        )
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
        [],
    ),
)
def test_participant_identifier_requires_exact_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="participant_id must be a string",
    ):
        Preparation(
            participant_id=value,
            publication_state=prepared_state(),
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
        Preparation(
            participant_id=value,
            publication_state=prepared_state(),
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
def test_opaque_nonblank_identifier_is_preserved(
    value: str,
) -> None:
    preparation = create_preparation(
        participant_id=value,
    )

    assert preparation.participant_id == value


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "state",
        b"state",
        1,
        True,
        (),
        [],
    ),
)
def test_publication_state_requires_nominal_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="publication_state",
    ):
        Preparation(
            participant_id="participant-001",
            publication_state=value,
        )


@pytest.mark.parametrize(
    "phase,revision",
    (
        (
            Phase.INTENT_RECORDED,
            1,
        ),
        (
            Phase.COMMIT_DECIDED,
            3,
        ),
        (
            Phase.COMMITTED,
            4,
        ),
        (
            Phase.ABORT_DECIDED,
            3,
        ),
        (
            Phase.ABORTED,
            4,
        ),
    ),
)
def test_only_prepared_phase_is_accepted(
    phase: Phase,
    revision: int,
) -> None:
    state = create_state(
        phase=phase,
        revision=revision,
    )

    with pytest.raises(
        ValueError,
        match="PREPARED phase",
    ):
        Preparation(
            participant_id="participant-001",
            publication_state=state,
        )


@pytest.mark.parametrize(
    "revision",
    (
        1,
        2,
        3,
        7,
        2**63,
        2**64 - 1,
    ),
)
def test_contract_preserves_any_valid_prepared_revision(
    revision: int,
) -> None:
    state = create_state(
        phase=Phase.PREPARED,
        revision=revision,
    )
    preparation = Preparation(
        participant_id="participant-001",
        publication_state=state,
    )

    assert (
        preparation.publication_state.revision
        == revision
    )


def test_preparation_preserves_signed_publication_intent() -> None:
    state = prepared_state()
    preparation = Preparation(
        participant_id="participant-001",
        publication_state=state,
    )

    assert (
        preparation
        .publication_state
        .publication_intent
        is state.publication_intent
    )


def test_preparation_defines_no_signature_of_its_own() -> None:
    hints = get_type_hints(Preparation)

    assert "signature" not in hints
    assert "signing_key_identity" not in hints


def test_preparation_defines_validation_only() -> None:
    import inspect

    source = inspect.getsource(
        Preparation
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


def test_preparation_imports_no_unsafe_capability() -> None:
    import inspect

    from sp001.services import (
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation,
    )

    source = inspect.getsource(
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation
    )

    assert "pickle" not in source
    assert "eval(" not in source
    assert "exec(" not in source
