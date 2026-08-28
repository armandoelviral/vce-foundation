from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from sp001.contracts.retail_process_actor import (
    ActorType,
    RetailProcessActor,
)
from sp001.contracts.retail_process_responsibility_assignment import (
    RetailProcessResponsibilityAssignment,
)
from sp001.contracts.retail_process_responsibility_verification import (
    ResponsibilityCoverageStatus,
    ResponsibilityEffectiveStatus,
    ResponsibilitySegregationStatus,
    RetailProcessResponsibilityVerificationPolicy,
    verify_retail_process_responsibility_assignment,
)
from sp001.contracts.retail_process_role import (
    RetailProcessRole,
)


EFFECTIVE_FROM = datetime(
    2026,
    8,
    1,
    tzinfo=timezone.utc,
)

EFFECTIVE_UNTIL = datetime(
    2026,
    9,
    1,
    tzinfo=timezone.utc,
)

ACTIVE_AT = datetime(
    2026,
    8,
    28,
    tzinfo=timezone.utc,
)


def create_actor(
    *,
    actor_id: str,
    customer_id: str = "CUSTOMER-A",
    actor_type: ActorType = ActorType.HUMAN,
) -> RetailProcessActor:
    return RetailProcessActor(
        actor_id=actor_id,
        customer_id=customer_id,
        actor_type=actor_type,
        organization_id="ORGANIZATION-A",
        role=RetailProcessRole(
            role_id=f"ROLE-{actor_id}",
            customer_id=customer_id,
            role_name=f"ROLE-{actor_id}",
        ),
    )


def create_assignment(
    *,
    responsible_actors: tuple[
        RetailProcessActor,
        ...,
    ] | None = None,
    accountable_actor: RetailProcessActor | None = None,
    consulted_actors: tuple[
        RetailProcessActor,
        ...,
    ] = (),
    informed_actors: tuple[
        RetailProcessActor,
        ...,
    ] = (),
    effective_from: datetime = EFFECTIVE_FROM,
    effective_until: datetime | None = EFFECTIVE_UNTIL,
) -> RetailProcessResponsibilityAssignment:
    return RetailProcessResponsibilityAssignment(
        responsibility_assignment_id="RACI-ASSIGNMENT-001",
        assignment_version=1,
        customer_id="CUSTOMER-A",
        process_type="EXPECTED_STATE_REVIEW",
        process_instance_id="EXPECTED-STATE-STORE-A",
        responsible_actors=(
            responsible_actors
            if responsible_actors is not None
            else (
                create_actor(
                    actor_id="ACTOR-RESPONSIBLE",
                ),
            )
        ),
        accountable_actor=(
            accountable_actor
            if accountable_actor is not None
            else create_actor(
                actor_id="ACTOR-ACCOUNTABLE",
            )
        ),
        effective_from=effective_from,
        effective_until=effective_until,
        source_governance_ids=(
            "GOVERNANCE-REFERENCE-001",
        ),
        consulted_actors=consulted_actors,
        informed_actors=informed_actors,
    )


def create_policy(
    **overrides: object,
) -> RetailProcessResponsibilityVerificationPolicy:
    values = {
        "verification_policy_id": "RACI-VERIFY-POLICY-001",
        "customer_id": "CUSTOMER-A",
        "require_consulted": False,
        "require_informed": False,
        "require_accountable_responsible_separation": True,
    }
    values.update(overrides)

    return RetailProcessResponsibilityVerificationPolicy(
        **values,
    )


def verify(
    *,
    assignment: RetailProcessResponsibilityAssignment | None = None,
    policy: RetailProcessResponsibilityVerificationPolicy | None = None,
    evaluated_at: datetime = ACTIVE_AT,
):
    return verify_retail_process_responsibility_assignment(
        assignment=(
            assignment
            if assignment is not None
            else create_assignment()
        ),
        policy=(
            policy
            if policy is not None
            else create_policy()
        ),
        evaluated_at=evaluated_at,
    )


def test_policy_preserves_customer_requirements() -> None:
    policy = create_policy(
        require_consulted=True,
        require_informed=True,
    )

    assert policy.verification_policy_id == (
        "RACI-VERIFY-POLICY-001"
    )
    assert policy.customer_id == "CUSTOMER-A"
    assert policy.require_consulted is True
    assert policy.require_informed is True
    assert (
        policy.require_accountable_responsible_separation
        is True
    )


def test_policy_is_immutable() -> None:
    policy = create_policy()

    with pytest.raises(FrozenInstanceError):
        policy.require_consulted = True


@pytest.mark.parametrize(
    "field, value",
    (
        ("verification_policy_id", ""),
        ("customer_id", " "),
    ),
)
def test_policy_rejects_empty_identity(
    field: str,
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        create_policy(
            **{
                field: value,
            },
        )


@pytest.mark.parametrize(
    "field",
    (
        "require_consulted",
        "require_informed",
        "require_accountable_responsible_separation",
    ),
)
def test_policy_rejects_untyped_boolean_requirements(
    field: str,
) -> None:
    with pytest.raises(
        TypeError,
        match=f"{field} must be a boolean",
    ):
        create_policy(
            **{
                field: 1,
            },
        )


def test_default_policy_has_complete_coverage() -> None:
    result = verify()

    assert result.coverage_status is (
        ResponsibilityCoverageStatus.COMPLETE
    )
    assert result.missing_participation_types == ()


def test_policy_can_require_consulted_participation() -> None:
    result = verify(
        policy=create_policy(
            require_consulted=True,
        ),
    )

    assert result.coverage_status is (
        ResponsibilityCoverageStatus.INCOMPLETE
    )
    assert result.missing_participation_types == (
        "CONSULTED",
    )


def test_policy_can_require_informed_participation() -> None:
    result = verify(
        policy=create_policy(
            require_informed=True,
        ),
    )

    assert result.coverage_status is (
        ResponsibilityCoverageStatus.INCOMPLETE
    )
    assert result.missing_participation_types == (
        "INFORMED",
    )


def test_required_consulted_and_informed_complete_coverage() -> None:
    assignment = create_assignment(
        consulted_actors=(
            create_actor(
                actor_id="ACTOR-CONSULTED",
            ),
        ),
        informed_actors=(
            create_actor(
                actor_id="ACTOR-INFORMED",
            ),
        ),
    )

    result = verify(
        assignment=assignment,
        policy=create_policy(
            require_consulted=True,
            require_informed=True,
        ),
    )

    assert result.coverage_status is (
        ResponsibilityCoverageStatus.COMPLETE
    )
    assert result.missing_participation_types == ()


def test_distinct_responsible_and_accountable_satisfy_segregation() -> None:
    result = verify()

    assert result.segregation_status is (
        ResponsibilitySegregationStatus.SATISFIED
    )
    assert result.segregation_conflict_actor_ids == ()


def test_same_actor_violates_required_segregation() -> None:
    actor = create_actor(
        actor_id="ACTOR-SHARED",
    )
    assignment = create_assignment(
        responsible_actors=(
            actor,
        ),
        accountable_actor=actor,
    )

    result = verify(
        assignment=assignment,
    )

    assert result.segregation_status is (
        ResponsibilitySegregationStatus.VIOLATED
    )
    assert result.segregation_conflict_actor_ids == (
        "ACTOR-SHARED",
    )


def test_policy_can_allow_responsible_accountable_overlap() -> None:
    actor = create_actor(
        actor_id="ACTOR-SHARED",
    )
    assignment = create_assignment(
        responsible_actors=(
            actor,
        ),
        accountable_actor=actor,
    )

    result = verify(
        assignment=assignment,
        policy=create_policy(
            require_accountable_responsible_separation=False,
        ),
    )

    assert result.segregation_status is (
        ResponsibilitySegregationStatus.SATISFIED
    )
    assert result.segregation_conflict_actor_ids == ()


def test_assignment_is_not_yet_effective_before_start() -> None:
    result = verify(
        evaluated_at=(
            EFFECTIVE_FROM
            - timedelta(
                seconds=1,
            )
        ),
    )

    assert result.effective_status is (
        ResponsibilityEffectiveStatus.NOT_YET_EFFECTIVE
    )


def test_assignment_is_active_exactly_at_start() -> None:
    result = verify(
        evaluated_at=EFFECTIVE_FROM,
    )

    assert result.effective_status is (
        ResponsibilityEffectiveStatus.ACTIVE
    )


def test_assignment_is_active_before_exclusive_end() -> None:
    result = verify(
        evaluated_at=(
            EFFECTIVE_UNTIL
            - timedelta(
                microseconds=1,
            )
        ),
    )

    assert result.effective_status is (
        ResponsibilityEffectiveStatus.ACTIVE
    )


def test_assignment_is_expired_exactly_at_exclusive_end() -> None:
    result = verify(
        evaluated_at=EFFECTIVE_UNTIL,
    )

    assert result.effective_status is (
        ResponsibilityEffectiveStatus.EXPIRED
    )


def test_open_ended_assignment_remains_active() -> None:
    assignment = create_assignment(
        effective_until=None,
    )

    result = verify(
        assignment=assignment,
        evaluated_at=(
            EFFECTIVE_FROM
            + timedelta(
                days=3650,
            )
        ),
    )

    assert result.effective_status is (
        ResponsibilityEffectiveStatus.ACTIVE
    )


def test_verification_rejects_untyped_assignment() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "assignment must be a "
            "RetailProcessResponsibilityAssignment"
        ),
    ):
        verify_retail_process_responsibility_assignment(
            assignment="RACI-ASSIGNMENT-001",
            policy=create_policy(),
            evaluated_at=ACTIVE_AT,
        )


def test_verification_rejects_untyped_policy() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "policy must be a "
            "RetailProcessResponsibilityVerificationPolicy"
        ),
    ):
        verify_retail_process_responsibility_assignment(
            assignment=create_assignment(),
            policy="RACI-VERIFY-POLICY-001",
            evaluated_at=ACTIVE_AT,
        )


def test_verification_rejects_cross_customer_policy() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "policy customer must match "
            "assignment customer"
        ),
    ):
        verify(
            policy=create_policy(
                customer_id="CUSTOMER-B",
            ),
        )


def test_verification_rejects_untyped_evaluation_time() -> None:
    with pytest.raises(
        TypeError,
        match="evaluated_at must be a datetime",
    ):
        verify(
            evaluated_at="2026-08-28T00:00:00Z",
        )


def test_verification_rejects_naive_evaluation_time() -> None:
    with pytest.raises(
        ValueError,
        match="evaluated_at must be timezone-aware",
    ):
        verify(
            evaluated_at=datetime(
                2026,
                8,
                28,
            ),
        )


def test_verification_preserves_exact_inputs() -> None:
    assignment = create_assignment()
    policy = create_policy()

    result = verify(
        assignment=assignment,
        policy=policy,
    )

    assert result.assignment is assignment
    assert result.policy is policy
    assert result.evaluated_at == ACTIVE_AT


def test_verification_does_not_mutate_assignment() -> None:
    assignment = create_assignment()
    original_responsible = assignment.responsible_actors
    original_accountable = assignment.accountable_actor

    verify(
        assignment=assignment,
    )

    assert assignment.responsible_actors == original_responsible
    assert assignment.accountable_actor is original_accountable


def test_verification_does_not_claim_authority_or_compliance() -> None:
    result = verify()

    for attribute in (
        "valid",
        "authority",
        "authority_verified",
        "authorization_status",
        "approved",
        "compliance_status",
        "commercial_outcome",
        "recommendation",
    ):
        assert not hasattr(
            result,
            attribute,
        )
