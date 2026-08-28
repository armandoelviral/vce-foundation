from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_process_actor import (
    ActorType,
    RetailProcessActor,
)
from sp001.contracts.retail_process_role import (
    RetailProcessRole,
)


def create_role(
    *,
    role_id: str = "ROLE-VM-REGIONAL",
    customer_id: str = "CUSTOMER-A",
    role_name: str = "REGIONAL_VISUAL_MERCHANDISER",
) -> RetailProcessRole:
    return RetailProcessRole(
        role_id=role_id,
        customer_id=customer_id,
        role_name=role_name,
    )


def create_actor(
    *,
    actor_id: str = "ACTOR-VM-001",
    customer_id: str = "CUSTOMER-A",
    actor_type: ActorType = ActorType.HUMAN,
    organization_id: str = "ORGANIZATION-A",
    role: RetailProcessRole | None = None,
) -> RetailProcessActor:
    return RetailProcessActor(
        actor_id=actor_id,
        customer_id=customer_id,
        actor_type=actor_type,
        organization_id=organization_id,
        role=(
            role
            if role is not None
            else create_role(
                customer_id=customer_id,
            )
        ),
    )


def test_actor_type_preserves_closed_categories() -> None:
    assert tuple(ActorType) == (
        ActorType.HUMAN,
        ActorType.TEAM,
        ActorType.SYSTEM,
        ActorType.ORGANIZATION,
    )


def test_role_preserves_explicit_identity() -> None:
    role = create_role()

    assert role.role_id == "ROLE-VM-REGIONAL"
    assert role.customer_id == "CUSTOMER-A"
    assert role.role_name == "REGIONAL_VISUAL_MERCHANDISER"


def test_role_is_immutable() -> None:
    role = create_role()

    with pytest.raises(FrozenInstanceError):
        role.role_name = "STORE_MANAGER"


@pytest.mark.parametrize(
    "field, value",
    (
        ("role_id", ""),
        ("customer_id", " "),
        ("role_name", None),
    ),
)
def test_role_rejects_empty_identity_fields(
    field: str,
    value: object,
) -> None:
    values = {
        "role_id": "ROLE-VM-REGIONAL",
        "customer_id": "CUSTOMER-A",
        "role_name": "REGIONAL_VISUAL_MERCHANDISER",
    }
    values[field] = value

    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        RetailProcessRole(**values)


def test_actor_preserves_explicit_identity_and_role() -> None:
    actor = create_actor()

    assert actor.actor_id == "ACTOR-VM-001"
    assert actor.customer_id == "CUSTOMER-A"
    assert actor.actor_type is ActorType.HUMAN
    assert actor.organization_id == "ORGANIZATION-A"
    assert actor.role.role_id == "ROLE-VM-REGIONAL"


def test_actor_is_immutable() -> None:
    actor = create_actor()

    with pytest.raises(FrozenInstanceError):
        actor.actor_id = "ACTOR-CHANGED"


@pytest.mark.parametrize(
    "field, value",
    (
        ("actor_id", ""),
        ("customer_id", " "),
        ("organization_id", None),
    ),
)
def test_actor_rejects_empty_identity_fields(
    field: str,
    value: object,
) -> None:
    values = {
        "actor_id": "ACTOR-VM-001",
        "customer_id": "CUSTOMER-A",
        "actor_type": ActorType.HUMAN,
        "organization_id": "ORGANIZATION-A",
        "role": create_role(),
    }
    values[field] = value

    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        RetailProcessActor(**values)


def test_actor_rejects_untyped_actor_category() -> None:
    with pytest.raises(
        TypeError,
        match="actor_type must be an ActorType",
    ):
        create_actor(
            actor_type="HUMAN",
        )


def test_actor_rejects_untyped_role() -> None:
    with pytest.raises(
        TypeError,
        match="role must be a RetailProcessRole",
    ):
        create_actor(
            role="ROLE-VM-REGIONAL",
        )


def test_actor_rejects_cross_customer_role() -> None:
    role = create_role(
        customer_id="CUSTOMER-B",
    )

    with pytest.raises(
        ValueError,
        match="role customer must match actor customer",
    ):
        create_actor(
            customer_id="CUSTOMER-A",
            role=role,
        )


@pytest.mark.parametrize(
    "actor_type",
    tuple(ActorType),
)
def test_every_actor_category_preserves_declared_type(
    actor_type: ActorType,
) -> None:
    actor = create_actor(
        actor_type=actor_type,
    )

    assert actor.actor_type is actor_type


def test_distinct_actor_identities_remain_distinct() -> None:
    actor_a = create_actor(
        actor_id="ACTOR-A",
    )
    actor_b = create_actor(
        actor_id="ACTOR-B",
    )

    assert actor_a != actor_b
    assert actor_a.actor_id != actor_b.actor_id


def test_equivalent_roles_can_exist_for_distinct_customers() -> None:
    role_a = create_role(
        role_id="ROLE-VM",
        customer_id="CUSTOMER-A",
    )
    role_b = create_role(
        role_id="ROLE-VM",
        customer_id="CUSTOMER-B",
    )

    assert role_a.role_name == role_b.role_name
    assert role_a.customer_id != role_b.customer_id
    assert role_a != role_b


def test_role_identity_does_not_grant_authority() -> None:
    role = create_role()

    for attribute in (
        "authority",
        "authority_source_ids",
        "permissions",
        "approval_scope",
        "delegation",
    ):
        assert not hasattr(
            role,
            attribute,
        )


def test_actor_identity_does_not_assign_raci_responsibility() -> None:
    actor = create_actor(
        actor_type=ActorType.SYSTEM,
    )

    for attribute in (
        "responsible",
        "accountable",
        "consulted",
        "informed",
        "raci_type",
        "authority",
        "approval",
    ):
        assert not hasattr(
            actor,
            attribute,
        )


def test_actor_identity_contains_no_personal_contact_fields() -> None:
    actor = create_actor()

    for attribute in (
        "name",
        "email",
        "phone",
        "address",
        "username",
    ):
        assert not hasattr(
            actor,
            attribute,
        )
