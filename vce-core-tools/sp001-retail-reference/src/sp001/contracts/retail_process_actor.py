from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_process_role import (
    RetailProcessRole,
)


class ActorType(StrEnum):
    """Closed actor categories without implied institutional authority."""

    HUMAN = "HUMAN"
    TEAM = "TEAM"
    SYSTEM = "SYSTEM"
    ORGANIZATION = "ORGANIZATION"


@dataclass(frozen=True, slots=True)
class RetailProcessActor:
    """Immutable actor identity within one customer-scoped process domain."""

    actor_id: str
    customer_id: str
    actor_type: ActorType
    organization_id: str
    role: RetailProcessRole

    def __post_init__(self) -> None:
        identity_fields = {
            "actor_id": self.actor_id,
            "customer_id": self.customer_id,
            "organization_id": self.organization_id,
        }

        for field, identity in identity_fields.items():
            if (
                not isinstance(
                    identity,
                    str,
                )
                or not identity.strip()
            ):
                raise ValueError(
                    f"{field} must not be empty"
                )

        if not isinstance(
            self.actor_type,
            ActorType,
        ):
            raise TypeError(
                "actor_type must be an ActorType"
            )

        if not isinstance(
            self.role,
            RetailProcessRole,
        ):
            raise TypeError(
                "role must be a RetailProcessRole"
            )

        if self.role.customer_id != self.customer_id:
            raise ValueError(
                "role customer must match actor customer"
            )
