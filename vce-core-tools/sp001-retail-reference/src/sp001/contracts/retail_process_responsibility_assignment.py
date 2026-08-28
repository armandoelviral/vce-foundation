from dataclasses import dataclass
from datetime import datetime

from sp001.contracts.retail_process_actor import (
    ActorType,
    RetailProcessActor,
)


@dataclass(frozen=True, slots=True)
class RetailProcessResponsibilityAssignment:
    """Versioned customer declaration of RACI process participation."""

    responsibility_assignment_id: str
    assignment_version: int
    customer_id: str
    process_type: str
    process_instance_id: str
    responsible_actors: tuple[RetailProcessActor, ...]
    accountable_actor: RetailProcessActor
    effective_from: datetime
    source_governance_ids: tuple[str, ...]
    consulted_actors: tuple[RetailProcessActor, ...] = ()
    informed_actors: tuple[RetailProcessActor, ...] = ()
    effective_until: datetime | None = None

    def __post_init__(self) -> None:
        identity_fields = {
            "responsibility_assignment_id": (
                self.responsibility_assignment_id
            ),
            "customer_id": self.customer_id,
            "process_type": self.process_type,
            "process_instance_id": self.process_instance_id,
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

        if (
            isinstance(
                self.assignment_version,
                bool,
            )
            or not isinstance(
                self.assignment_version,
                int,
            )
            or self.assignment_version < 1
        ):
            raise ValueError(
                "assignment_version must be a positive integer"
            )

        actor_collections = (
            (
                "responsible_actors",
                self.responsible_actors,
            ),
            (
                "consulted_actors",
                self.consulted_actors,
            ),
            (
                "informed_actors",
                self.informed_actors,
            ),
        )

        for collection_name, actors in actor_collections:
            if not isinstance(
                actors,
                tuple,
            ):
                raise TypeError(
                    f"{collection_name} must be an immutable tuple"
                )

            seen_actor_ids: set[str] = set()

            for actor in actors:
                if not isinstance(
                    actor,
                    RetailProcessActor,
                ):
                    raise TypeError(
                        f"{collection_name} must contain "
                        "RetailProcessActor values"
                    )

                if actor.customer_id != self.customer_id:
                    raise ValueError(
                        f"{collection_name} actor customer "
                        "must match assignment customer"
                    )

                if actor.actor_id in seen_actor_ids:
                    raise ValueError(
                        f"duplicate {collection_name} actor_id: "
                        f"{actor.actor_id}"
                    )

                seen_actor_ids.add(
                    actor.actor_id,
                )

        if not self.responsible_actors:
            raise ValueError(
                "responsible_actors must not be empty"
            )

        if not isinstance(
            self.accountable_actor,
            RetailProcessActor,
        ):
            raise TypeError(
                "accountable_actor must be a RetailProcessActor"
            )

        if (
            self.accountable_actor.customer_id
            != self.customer_id
        ):
            raise ValueError(
                "accountable actor customer "
                "must match assignment customer"
            )

        if (
            self.accountable_actor.actor_type
            is ActorType.SYSTEM
        ):
            raise ValueError(
                "SYSTEM actor cannot be accountable"
            )

        self._validate_effective_datetime(
            field="effective_from",
            value=self.effective_from,
        )

        if self.effective_until is not None:
            self._validate_effective_datetime(
                field="effective_until",
                value=self.effective_until,
            )

            if self.effective_until <= self.effective_from:
                raise ValueError(
                    "effective_until must be after effective_from"
                )

        if not isinstance(
            self.source_governance_ids,
            tuple,
        ):
            raise TypeError(
                "source_governance_ids must be an immutable tuple"
            )

        if not self.source_governance_ids:
            raise ValueError(
                "source_governance_ids must not be empty"
            )

        seen_source_ids: set[str] = set()

        for source_id in self.source_governance_ids:
            if (
                not isinstance(
                    source_id,
                    str,
                )
                or not source_id.strip()
            ):
                raise ValueError(
                    "source governance_id must not be empty"
                )

            if source_id in seen_source_ids:
                raise ValueError(
                    "duplicate source governance_id: "
                    f"{source_id}"
                )

            seen_source_ids.add(
                source_id,
            )

    @staticmethod
    def _validate_effective_datetime(
        *,
        field: str,
        value: object,
    ) -> None:
        if not isinstance(
            value,
            datetime,
        ):
            raise TypeError(
                f"{field} must be a datetime"
            )

        if (
            value.tzinfo is None
            or value.utcoffset() is None
        ):
            raise ValueError(
                f"{field} must be timezone-aware"
            )
