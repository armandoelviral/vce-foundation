from dataclasses import dataclass

from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


@dataclass(frozen=True, slots=True)
class RetailExpectedState:
    """Explicit, versioned expectation for one customer-scoped retail context."""

    expected_state_id: str
    expected_state_version: int
    snapshot: RetailContextSnapshot
    expectation_type: str
    expected_value: str
    source_dimension_ids: tuple[str, ...]
    source_policy_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if (
            not isinstance(
                self.expected_state_id,
                str,
            )
            or not self.expected_state_id.strip()
        ):
            raise ValueError(
                "expected_state_id must not be empty"
            )

        if (
            isinstance(
                self.expected_state_version,
                bool,
            )
            or not isinstance(
                self.expected_state_version,
                int,
            )
            or self.expected_state_version < 1
        ):
            raise ValueError(
                "expected_state_version must be "
                "a positive integer"
            )

        if not isinstance(
            self.snapshot,
            RetailContextSnapshot,
        ):
            raise TypeError(
                "snapshot must be a RetailContextSnapshot"
            )

        if self.snapshot.context_scope is None:
            raise ValueError(
                "expected state requires context_scope"
            )

        if self.snapshot.context_definition is None:
            raise ValueError(
                "expected state requires context_definition"
            )

        if (
            not isinstance(
                self.expectation_type,
                str,
            )
            or not self.expectation_type.strip()
        ):
            raise ValueError(
                "expectation_type must not be empty"
            )

        if (
            not isinstance(
                self.expected_value,
                str,
            )
            or not self.expected_value.strip()
        ):
            raise ValueError(
                "expected_value must not be empty"
            )

        if not isinstance(
            self.source_dimension_ids,
            tuple,
        ):
            raise TypeError(
                "source_dimension_ids must be "
                "an immutable tuple"
            )

        if not self.source_dimension_ids:
            raise ValueError(
                "source_dimension_ids must not be empty"
            )

        available_dimension_ids = {
            dimension.dimension_id
            for dimension in self.snapshot.dimensions
        }

        seen_dimension_ids: set[str] = set()

        for dimension_id in self.source_dimension_ids:
            if (
                not isinstance(
                    dimension_id,
                    str,
                )
                or not dimension_id.strip()
            ):
                raise ValueError(
                    "source dimension_id must not be empty"
                )

            if dimension_id in seen_dimension_ids:
                raise ValueError(
                    "duplicate source dimension_id: "
                    f"{dimension_id}"
                )

            if dimension_id not in available_dimension_ids:
                raise ValueError(
                    "source dimension_id not present "
                    "in snapshot: "
                    f"{dimension_id}"
                )

            seen_dimension_ids.add(
                dimension_id,
            )

        if not isinstance(
            self.source_policy_ids,
            tuple,
        ):
            raise TypeError(
                "source_policy_ids must be "
                "an immutable tuple"
            )

        seen_policy_ids: set[str] = set()

        for policy_id in self.source_policy_ids:
            if (
                not isinstance(
                    policy_id,
                    str,
                )
                or not policy_id.strip()
            ):
                raise ValueError(
                    "source policy_id must not be empty"
                )

            if policy_id in seen_policy_ids:
                raise ValueError(
                    "duplicate source policy_id: "
                    f"{policy_id}"
                )

            seen_policy_ids.add(
                policy_id,
            )
