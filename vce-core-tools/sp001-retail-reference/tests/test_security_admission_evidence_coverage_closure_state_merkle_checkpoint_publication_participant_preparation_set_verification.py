import inspect

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set_verification import (
    verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    prepared_state,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    Participant,
)


ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)
Preparation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
verify = (
    verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set
)


def participant_id(
    index: int,
) -> str:
    return f"participant-{index:03d}"


def participant_set(
    indices,
):
    return ParticipantSet(
        participants=tuple(
            Participant(
                participant_id(index)
            )
            for index in indices
        ),
    )


def preparation_set(
    indices,
):
    state = prepared_state()

    return PreparationSet(
        preparations=tuple(
            Preparation(
                participant_id=(
                    participant_id(index)
                ),
                publication_state=state,
            )
            for index in indices
        ),
    )


@pytest.mark.parametrize(
    "indices",
    (
        (1,),
        (1, 2),
        (1, 2, 3),
        (1, 2, 3, 4, 5),
        tuple(range(1, 11)),
    ),
)
def test_exact_roster_coverage_verifies(
    indices,
) -> None:
    assert (
        verify(
            participant_set=(
                participant_set(indices)
            ),
            preparation_set=(
                preparation_set(indices)
            ),
        )
        is True
    )


def test_result_is_nominal_bool() -> None:
    result = verify(
        participant_set=(
            participant_set((1,))
        ),
        preparation_set=(
            preparation_set((1,))
        ),
    )

    assert type(result) is bool


@pytest.mark.parametrize(
    "roster_indices,prepared_indices",
    (
        (
            (1, 2),
            (1,),
        ),
        (
            (1, 2, 3),
            (1, 2),
        ),
        (
            (1, 2, 3, 4),
            (1, 2, 3),
        ),
    ),
)
def test_missing_participant_fails_closed(
    roster_indices,
    prepared_indices,
) -> None:
    assert (
        verify(
            participant_set=(
                participant_set(
                    roster_indices
                )
            ),
            preparation_set=(
                preparation_set(
                    prepared_indices
                )
            ),
        )
        is False
    )


@pytest.mark.parametrize(
    "roster_indices,prepared_indices",
    (
        (
            (1,),
            (1, 2),
        ),
        (
            (1, 2),
            (1, 2, 3),
        ),
        (
            (1, 2, 3),
            (1, 2, 3, 4),
        ),
    ),
)
def test_extra_participant_fails_closed(
    roster_indices,
    prepared_indices,
) -> None:
    assert (
        verify(
            participant_set=(
                participant_set(
                    roster_indices
                )
            ),
            preparation_set=(
                preparation_set(
                    prepared_indices
                )
            ),
        )
        is False
    )


@pytest.mark.parametrize(
    "roster_indices,prepared_indices",
    (
        (
            (1,),
            (2,),
        ),
        (
            (1, 2),
            (1, 3),
        ),
        (
            (1, 2, 3),
            (1, 2, 4),
        ),
        (
            (1, 3, 5),
            (1, 3, 6),
        ),
    ),
)
def test_same_cardinality_with_substitution_fails_closed(
    roster_indices,
    prepared_indices,
) -> None:
    assert (
        len(roster_indices)
        == len(prepared_indices)
    )

    assert (
        verify(
            participant_set=(
                participant_set(
                    roster_indices
                )
            ),
            preparation_set=(
                preparation_set(
                    prepared_indices
                )
            ),
        )
        is False
    )


def test_prefix_similarity_does_not_authorize() -> None:
    assert (
        verify(
            participant_set=(
                participant_set(
                    (1, 2, 3)
                )
            ),
            preparation_set=(
                preparation_set(
                    (1, 2)
                )
            ),
        )
        is False
    )


def test_superset_similarity_does_not_authorize() -> None:
    assert (
        verify(
            participant_set=(
                participant_set(
                    (1, 2)
                )
            ),
            preparation_set=(
                preparation_set(
                    (1, 2, 3)
                )
            ),
        )
        is False
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        (),
        [],
        {},
        "participant-set",
        b"participant-set",
        1,
        True,
    ),
)
def test_participant_set_requires_nominal_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="participant_set",
    ):
        verify(
            participant_set=value,
            preparation_set=(
                preparation_set((1,))
            ),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        (),
        [],
        {},
        "preparation-set",
        b"preparation-set",
        1,
        True,
    ),
)
def test_preparation_set_requires_nominal_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="preparation_set",
    ):
        verify(
            participant_set=(
                participant_set((1,))
            ),
            preparation_set=value,
        )


def test_verification_does_not_invoke_participant_operations() -> None:
    roster = participant_set(
        (1, 2, 3)
    )
    preparations = preparation_set(
        (1, 2, 3)
    )

    assert verify(
        participant_set=roster,
        preparation_set=preparations,
    )


def test_verification_has_exact_keyword_only_surface() -> None:
    signature = inspect.signature(verify)

    assert tuple(signature.parameters) == (
        "participant_set",
        "preparation_set",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter
        in signature.parameters.values()
    )
    assert signature.return_annotation is bool


def test_verification_defines_comparison_only() -> None:
    source = inspect.getsource(
        verify
    ).lower()

    for forbidden in (
        "prepare(",
        "commit(",
        "abort(",
        "append(",
        "sort(",
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


def test_verification_imports_no_unsafe_capability() -> None:
    from sp001.services import (
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set_verification,
    )

    source = inspect.getsource(
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set_verification
    )

    assert "pickle" not in source
    assert "eval(" not in source
    assert "exec(" not in source
