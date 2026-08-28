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
from sp001.contracts.retail_process_role import (
    RetailProcessRole,
)


EFFECTIVE_FROM = datetime(
    2026,
    8,
    28,
    0,
    0,
    tzinfo=timezone.utc,
)


def create_actor(
    *,
    actor_id: str,
    customer_id: str = "CUSTOMER-A",
    actor_type: ActorType = ActorType.HUMAN,
    role_id: str = "ROLE-VM",
) -> RetailProcessActor:
    return RetailProcessActor(
        actor_id=actor_id,
        customer_id=customer_id,
        actor_type=actor_type,
        organization_id=f"ORGANIZATION-{customer_id}",
        role=RetailProcessRole(
            role_id=role_id,
            customer_id=customer_id,
            role_name=role_id,
        ),
    )


def create_assignment(
    **overrides: object,
) -> RetailProcessResponsibilityAssignment:
    values = {
        "responsibility_assignment_id": "RACI-ASSIGNMENT-001",
        "assignment_version": 1,
        "customer_id": "CUSTOMER-A",
        "process_type": "RETAIL_EXPECTED_STATE_REVIEW",
        "process_instance_id": "EXPECTED-STATE-STORE-A",
        "responsible_actors": (
            create_actor(
                actor_id="ACTOR-VM-001",
            ),
        ),
        "accountable_actor": create_actor(
            actor_id="ACTOR-DIRECTOR-001",
            role_id="ROLE-VM-DIRECTOR",
        ),
        "effective_from": EFFECTIVE_FROM,
        "source_governance_ids": (
            "GOVERNANCE-POLICY-001",
        ),
        "consulted_actors": (
            create_actor(
                actor_id="ACTOR-OPERATIONS-001",
                actor_type=ActorType.TEAM,
                role_id="ROLE-OPERATIONS",
            ),
        ),
        "informed_actors": (
            create_actor(
                actor_id="ACTOR-STORE-001",
                actor_type=ActorType.TEAM,
                role_id="ROLE-STORE",
            ),
        ),
        "effective_until": None,
    }
    values.update(overrides)

    return RetailProcessResponsibilityAssignment(
        **values,
    )


def test_assignment_preserves_versioned_process_identity() -> None:
    assignment = create_assignment()

    assert assignment.responsibility_assignment_id == (
        "RACI-ASSIGNMENT-001"
    )
    assert assignment.assignment_version == 1
    assert assignment.customer_id == "CUSTOMER-A"
    assert assignment.process_type == (
        "RETAIL_EXPECTED_STATE_REVIEW"
    )
    assert assignment.process_instance_id == (
        "EXPECTED-STATE-STORE-A"
    )


def test_assignment_preserves_all_raci_participants() -> None:
    assignment = create_assignment()

    assert assignment.responsible_actors[0].actor_id == (
        "ACTOR-VM-001"
    )
    assert assignment.accountable_actor.actor_id == (
        "ACTOR-DIRECTOR-001"
    )
    assert assignment.consulted_actors[0].actor_id == (
        "ACTOR-OPERATIONS-001"
    )
    assert assignment.informed_actors[0].actor_id == (
        "ACTOR-STORE-001"
    )


def test_assignment_is_immutable() -> None:
    assignment = create_assignment()

    with pytest.raises(FrozenInstanceError):
        assignment.assignment_version = 2


@pytest.mark.parametrize(
    "field, value",
    (
        ("responsibility_assignment_id", ""),
        ("customer_id", " "),
        ("process_type", None),
        ("process_instance_id", ""),
    ),
)
def test_assignment_rejects_empty_identity_fields(
    field: str,
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        create_assignment(
            **{
                field: value,
            },
        )


@pytest.mark.parametrize(
    "version",
    (
        True,
        0,
        -1,
        1.0,
        "1",
    ),
)
def test_assignment_rejects_invalid_versions(
    version: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "assignment_version must be "
            "a positive integer"
        ),
    ):
        create_assignment(
            assignment_version=version,
        )


@pytest.mark.parametrize(
    "field",
    (
        "responsible_actors",
        "consulted_actors",
        "informed_actors",
    ),
)
def test_assignment_rejects_mutable_actor_collections(
    field: str,
) -> None:
    with pytest.raises(
        TypeError,
        match=f"{field} must be an immutable tuple",
    ):
        create_assignment(
            **{
                field: [],
            },
        )


def test_assignment_requires_at_least_one_responsible_actor() -> None:
    with pytest.raises(
        ValueError,
        match="responsible_actors must not be empty",
    ):
        create_assignment(
            responsible_actors=(),
        )


@pytest.mark.parametrize(
    "field",
    (
        "responsible_actors",
        "consulted_actors",
        "informed_actors",
    ),
)
def test_assignment_rejects_untyped_actor_members(
    field: str,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            f"{field} must contain "
            "RetailProcessActor values"
        ),
    ):
        create_assignment(
            **{
                field: (
                    "ACTOR-001",
                ),
            },
        )


@pytest.mark.parametrize(
    "field",
    (
        "responsible_actors",
        "consulted_actors",
        "informed_actors",
    ),
)
def test_assignment_rejects_cross_customer_participants(
    field: str,
) -> None:
    actor = create_actor(
        actor_id="ACTOR-CUSTOMER-B",
        customer_id="CUSTOMER-B",
    )

    with pytest.raises(
        ValueError,
        match=(
            f"{field} actor customer "
            "must match assignment customer"
        ),
    ):
        create_assignment(
            **{
                field: (
                    actor,
                ),
            },
        )


@pytest.mark.parametrize(
    "field",
    (
        "responsible_actors",
        "consulted_actors",
        "informed_actors",
    ),
)
def test_assignment_rejects_duplicate_actor_within_category(
    field: str,
) -> None:
    actor = create_actor(
        actor_id="ACTOR-DUPLICATE",
    )

    with pytest.raises(
        ValueError,
        match=f"duplicate {field} actor_id",
    ):
        create_assignment(
            **{
                field: (
                    actor,
                    actor,
                ),
            },
        )


def test_assignment_rejects_untyped_accountable_actor() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "accountable_actor must be "
            "a RetailProcessActor"
        ),
    ):
        create_assignment(
            accountable_actor="ACTOR-DIRECTOR-001",
        )


def test_assignment_rejects_cross_customer_accountable_actor() -> None:
    actor = create_actor(
        actor_id="ACTOR-CUSTOMER-B",
        customer_id="CUSTOMER-B",
    )

    with pytest.raises(
        ValueError,
        match=(
            "accountable actor customer "
            "must match assignment customer"
        ),
    ):
        create_assignment(
            accountable_actor=actor,
        )


def test_system_actor_cannot_be_accountable() -> None:
    actor = create_actor(
        actor_id="ACTOR-AUTOMATION-001",
        actor_type=ActorType.SYSTEM,
        role_id="ROLE-AUTOMATION",
    )

    with pytest.raises(
        ValueError,
        match="SYSTEM actor cannot be accountable",
    ):
        create_assignment(
            accountable_actor=actor,
        )


def test_system_actor_can_be_responsible_for_execution() -> None:
    actor = create_actor(
        actor_id="ACTOR-RULE-ENGINE-001",
        actor_type=ActorType.SYSTEM,
        role_id="ROLE-RULE-EVALUATOR",
    )

    assignment = create_assignment(
        responsible_actors=(
            actor,
        ),
    )

    assert assignment.responsible_actors == (
        actor,
    )
    assert assignment.accountable_actor.actor_type is (
        ActorType.HUMAN
    )


def test_assignment_preserves_timezone_aware_effective_interval() -> None:
    effective_until = (
        EFFECTIVE_FROM
        + timedelta(
            days=30,
        )
    )

    assignment = create_assignment(
        effective_until=effective_until,
    )

    assert assignment.effective_from == EFFECTIVE_FROM
    assert assignment.effective_until == effective_until


@pytest.mark.parametrize(
    "field",
    (
        "effective_from",
        "effective_until",
    ),
)
def test_assignment_rejects_untyped_effective_datetime(
    field: str,
) -> None:
    with pytest.raises(
        TypeError,
        match=f"{field} must be a datetime",
    ):
        create_assignment(
            **{
                field: "2026-08-28T00:00:00Z",
            },
        )


@pytest.mark.parametrize(
    "field",
    (
        "effective_from",
        "effective_until",
    ),
)
def test_assignment_rejects_naive_effective_datetime(
    field: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must be timezone-aware",
    ):
        create_assignment(
            **{
                field: datetime(
                    2026,
                    8,
                    28,
                ),
            },
        )


def test_assignment_rejects_non_increasing_effective_interval() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "effective_until must be "
            "after effective_from"
        ),
    ):
        create_assignment(
            effective_until=EFFECTIVE_FROM,
        )


def test_assignment_requires_governance_sources() -> None:
    with pytest.raises(
        ValueError,
        match="source_governance_ids must not be empty",
    ):
        create_assignment(
            source_governance_ids=(),
        )


def test_assignment_rejects_mutable_governance_sources() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "source_governance_ids must be "
            "an immutable tuple"
        ),
    ):
        create_assignment(
            source_governance_ids=[
                "GOVERNANCE-POLICY-001",
            ],
        )


def test_assignment_rejects_duplicate_governance_sources() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate source governance_id",
    ):
        create_assignment(
            source_governance_ids=(
                "GOVERNANCE-POLICY-001",
                "GOVERNANCE-POLICY-001",
            ),
        )


def test_assignment_does_not_claim_verified_authority() -> None:
    assignment = create_assignment()

    for attribute in (
        "authority_verified",
        "authorization_status",
        "approved",
        "approval",
        "compliance_status",
        "commercial_outcome",
        "signature",
    ):
        assert not hasattr(
            assignment,
            attribute,
        )
