from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_rule_observation import (
    RuleObservationStatus,
    RetailContextRuleObservation,
)


def build_observation(
    *,
    observation_id: str = "OBSERVATION-001",
    rule_id: str = "RULE-FIXTURE-001",
    snapshot_id: str = "RCP-SNAPSHOT-001",
    snapshot_version: int = 1,
    case_id: str = "CASE-001",
    status: RuleObservationStatus = (
        RuleObservationStatus.CONFORMANT
    ),
    evidence_ids: tuple[str, ...] = ("ART-002",),
) -> RetailContextRuleObservation:
    return RetailContextRuleObservation(
        observation_id=observation_id,
        rule_id=rule_id,
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        case_id=case_id,
        status=status,
        evidence_ids=evidence_ids,
    )


def test_observation_preserves_identity_and_rule_reference() -> None:
    observation = build_observation()

    assert observation.observation_id == "OBSERVATION-001"
    assert observation.rule_id == "RULE-FIXTURE-001"


def test_observation_preserves_snapshot_and_case_identity() -> None:
    observation = build_observation()

    assert observation.snapshot_id == "RCP-SNAPSHOT-001"
    assert observation.snapshot_version == 1
    assert observation.case_id == "CASE-001"


def test_conformant_observation_preserves_evidence_reference() -> None:
    observation = build_observation(
        status=RuleObservationStatus.CONFORMANT,
        evidence_ids=("ART-002",),
    )

    assert observation.status is RuleObservationStatus.CONFORMANT
    assert observation.evidence_ids == ("ART-002",)


def test_non_conformant_observation_preserves_evidence_reference() -> None:
    observation = build_observation(
        status=RuleObservationStatus.NON_CONFORMANT,
        evidence_ids=("ART-003",),
    )

    assert (
        observation.status
        is RuleObservationStatus.NON_CONFORMANT
    )

    assert observation.evidence_ids == ("ART-003",)


def test_insufficient_evidence_does_not_require_invented_reference() -> None:
    observation = build_observation(
        status=RuleObservationStatus.INSUFFICIENT_EVIDENCE,
        evidence_ids=(),
    )

    assert observation.evidence_ids == ()


def test_disputed_observation_does_not_require_invented_reference() -> None:
    observation = build_observation(
        status=RuleObservationStatus.DISPUTED,
        evidence_ids=(),
    )

    assert observation.status is RuleObservationStatus.DISPUTED
    assert observation.evidence_ids == ()


@pytest.mark.parametrize(
    "status",
    (
        RuleObservationStatus.CONFORMANT,
        RuleObservationStatus.NON_CONFORMANT,
    ),
)
def test_conclusive_observation_requires_evidence(
    status: RuleObservationStatus,
) -> None:
    with pytest.raises(
        ValueError,
        match="conclusive observation requires evidence",
    ):
        build_observation(
            status=status,
            evidence_ids=(),
        )


@pytest.mark.parametrize(
    "field",
    (
        "observation_id",
        "rule_id",
        "snapshot_id",
        "case_id",
    ),
)
@pytest.mark.parametrize(
    "invalid_identity",
    ("", "   "),
)
def test_observation_rejects_invalid_identity(
    field: str,
    invalid_identity: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        build_observation(
            **{
                field: invalid_identity,
            }
        )


@pytest.mark.parametrize(
    "invalid_version",
    (0, -1, True),
)
def test_observation_rejects_invalid_snapshot_version(
    invalid_version: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="snapshot_version must be a positive integer",
    ):
        build_observation(
            snapshot_version=invalid_version,
        )


def test_observation_rejects_untyped_status() -> None:
    with pytest.raises(
        TypeError,
        match="status must be a RuleObservationStatus",
    ):
        build_observation(
            status="CONFORMANT",
        )


def test_observation_rejects_mutable_evidence_collection() -> None:
    with pytest.raises(
        TypeError,
        match="evidence_ids must be an immutable tuple",
    ):
        build_observation(
            evidence_ids=["ART-002"],
        )


@pytest.mark.parametrize(
    "invalid_evidence_id",
    ("", "   ", 123),
)
def test_observation_rejects_invalid_evidence_identity(
    invalid_evidence_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="evidence_id must not be empty",
    ):
        build_observation(
            evidence_ids=(invalid_evidence_id,),
        )


def test_observation_rejects_duplicate_evidence_identity() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate evidence_id: ART-002",
    ):
        build_observation(
            evidence_ids=("ART-002", "ART-002"),
        )


def test_observation_preserves_evidence_order() -> None:
    observation = build_observation(
        evidence_ids=("ART-003", "ART-002"),
    )

    assert observation.evidence_ids == (
        "ART-003",
        "ART-002",
    )


def test_observation_is_immutable() -> None:
    observation = build_observation()

    with pytest.raises(FrozenInstanceError):
        observation.rule_id = "RULE-FIXTURE-002"


def test_observation_does_not_claim_customer_acceptance() -> None:
    assert "ACCEPTED" not in {
        status.value
        for status in RuleObservationStatus
    }

    assert "CUSTOMER_APPROVED" not in {
        status.value
        for status in RuleObservationStatus
    }


def test_observation_vocabulary_is_exact() -> None:
    assert {
        status.value
        for status in RuleObservationStatus
    } == {
        "CONFORMANT",
        "NON_CONFORMANT",
        "INSUFFICIENT_EVIDENCE",
        "DISPUTED",
    }
