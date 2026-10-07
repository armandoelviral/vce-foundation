import inspect
from dataclasses import replace

import pytest

import sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_derivation as derivation_module
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    create_components,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
derive = (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision
)


def derive_from_components(
    *,
    size: int = 3,
):
    (
        publication_intent,
        participant_set,
        preparation_set,
    ) = create_components(
        size=size,
    )

    record = derive(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=preparation_set,
    )

    return (
        publication_intent,
        participant_set,
        preparation_set,
        record,
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
def test_exact_preparation_coverage_derives_commit(
    size: int,
) -> None:
    *_, record = derive_from_components(
        size=size,
    )

    assert record.decision is Decision.COMMIT


def test_derivation_returns_nominal_decision_record() -> None:
    *_, record = derive_from_components()

    assert isinstance(record, DecisionRecord)


def test_derivation_preserves_exact_evidence_graph() -> None:
    (
        publication_intent,
        participant_set,
        preparation_set,
        record,
    ) = derive_from_components()

    assert record.publication_intent is publication_intent
    assert record.participant_set is participant_set
    assert record.preparation_set is preparation_set


@pytest.mark.parametrize(
    "retained_count",
    (
        1,
        2,
    ),
)
def test_missing_preparation_derives_abort(
    retained_count: int,
) -> None:
    (
        publication_intent,
        participant_set,
        complete_set,
    ) = create_components(
        size=3,
    )
    incomplete_set = PreparationSet(
        preparations=complete_set.preparations[
            :retained_count
        ],
    )

    record = derive(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=incomplete_set,
    )

    assert record.decision is Decision.ABORT


def test_unknown_prepared_participant_derives_abort() -> None:
    (
        publication_intent,
        participant_set,
        complete_set,
    ) = create_components(
        size=3,
    )
    changed_preparations = (
        complete_set.preparations[:2]
        + (
            replace(
                complete_set.preparations[2],
                participant_id="participant-999",
            ),
        )
    )
    changed_set = PreparationSet(
        preparations=changed_preparations,
    )

    record = derive(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=changed_set,
    )

    assert record.decision is Decision.ABORT


def test_extra_preparation_derives_abort() -> None:
    (
        publication_intent,
        _,
        preparation_set,
    ) = create_components(
        size=4,
    )
    (
        _,
        participant_set,
        _,
    ) = create_components(
        size=3,
    )

    record = derive(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=preparation_set,
    )

    assert record.decision is Decision.ABORT


def test_same_cardinality_with_different_roster_derives_abort() -> None:
    (
        publication_intent,
        participant_set,
        complete_set,
    ) = create_components(
        size=3,
    )
    changed_set = PreparationSet(
        preparations=(
            replace(
                complete_set.preparations[0],
                participant_id="participant-000",
            ),
            *complete_set.preparations[:2],
        ),
    )

    record = derive(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=changed_set,
    )

    assert record.decision is Decision.ABORT


def test_preparation_from_other_publication_is_rejected() -> None:
    (
        _,
        participant_set,
        preparation_set,
    ) = create_components()

    with pytest.raises(
        ValueError,
        match="exact publication intent",
    ):
        derive(
            publication_intent=create_intent(
                publication_id="publication-other",
                scalar=2,
            ),
            participant_set=participant_set,
            preparation_set=preparation_set,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "publication-intent",
        1,
        True,
        (),
    ),
)
def test_publication_intent_rejects_invalid_type(
    value: object,
) -> None:
    (
        _,
        participant_set,
        preparation_set,
    ) = create_components()

    with pytest.raises(
        TypeError,
        match="publication_intent",
    ):
        derive(
            publication_intent=value,
            participant_set=participant_set,
            preparation_set=preparation_set,
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
    (
        publication_intent,
        _,
        preparation_set,
    ) = create_components()

    with pytest.raises(
        TypeError,
        match="participant_set",
    ):
        derive(
            publication_intent=publication_intent,
            participant_set=value,
            preparation_set=preparation_set,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "preparation-set",
        1,
        True,
        (),
    ),
)
def test_preparation_set_rejects_invalid_type(
    value: object,
) -> None:
    (
        publication_intent,
        participant_set,
        _,
    ) = create_components()

    with pytest.raises(
        TypeError,
        match="preparation_set",
    ):
        derive(
            publication_intent=publication_intent,
            participant_set=participant_set,
            preparation_set=value,
        )


@pytest.mark.parametrize(
    "invalid_result",
    (
        None,
        0,
        1,
        "true",
        object(),
    ),
)
def test_non_boolean_verification_result_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
    invalid_result: object,
) -> None:
    (
        publication_intent,
        participant_set,
        preparation_set,
    ) = create_components()

    monkeypatch.setattr(
        derivation_module,
        "verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set",
        lambda **_: invalid_result,
    )

    with pytest.raises(
        TypeError,
        match="must return a bool",
    ):
        derive(
            publication_intent=publication_intent,
            participant_set=participant_set,
            preparation_set=preparation_set,
        )


def test_derivation_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(derive)

    assert tuple(signature.parameters) == (
        "publication_intent",
        "participant_set",
        "preparation_set",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )
    assert signature.return_annotation is DecisionRecord


def test_derivation_defines_no_participant_effects_or_persistence() -> None:
    source = inspect.getsource(derive).lower()

    for forbidden in (
        ".prepare(",
        ".commit(",
        ".abort(",
        "sqlite",
        "database",
        "compare_and_swap",
        "network",
        "http",
        "socket",
    ):
        assert forbidden not in source
