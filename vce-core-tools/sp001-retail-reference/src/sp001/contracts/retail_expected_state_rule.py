from dataclasses import dataclass

from sp001.contracts.retail_context_definition import (
    RetailContextDefinition,
)


@dataclass(frozen=True, slots=True)
class RetailExpectedStateRule:
    """Immutable customer-declared conditions for one expected state."""

    expected_state_rule_id: str
    expected_state_rule_version: int
    context_definition: RetailContextDefinition
    expectation_type: str
    expected_value: str
    required_dimension_values: tuple[
        tuple[str, str],
        ...,
    ]
    source_policy_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if (
            not isinstance(
                self.expected_state_rule_id,
                str,
            )
            or not self.expected_state_rule_id.strip()
        ):
            raise ValueError(
                "expected_state_rule_id "
                "must not be empty"
            )

        if (
            isinstance(
                self.expected_state_rule_version,
                bool,
            )
            or not isinstance(
                self.expected_state_rule_version,
                int,
            )
            or self.expected_state_rule_version < 1
        ):
            raise ValueError(
                "expected_state_rule_version "
                "must be a positive integer"
            )

        if not isinstance(
            self.context_definition,
            RetailContextDefinition,
        ):
            raise TypeError(
                "context_definition must be a "
                "RetailContextDefinition"
            )

        if (
            not isinstance(
                self.expectation_type,
                str,
            )
            or not self.expectation_type.strip()
        ):
            raise ValueError(
                "expectation_type "
                "must not be empty"
            )

        if (
            not isinstance(
                self.expected_value,
                str,
            )
            or not self.expected_value.strip()
        ):
            raise ValueError(
                "expected_value "
                "must not be empty"
            )

        if not isinstance(
            self.required_dimension_values,
            tuple,
        ):
            raise TypeError(
                "required_dimension_values "
                "must be an immutable tuple"
            )

        if not self.required_dimension_values:
            raise ValueError(
                "required_dimension_values "
                "must not be empty"
            )

        seen_dimension_types: set[str] = set()

        for condition in (
            self.required_dimension_values
        ):
            if (
                not isinstance(
                    condition,
                    tuple,
                )
                or len(
                    condition,
                )
                != 2
            ):
                raise TypeError(
                    "dimension condition must be "
                    "an immutable type-value pair"
                )

            dimension_type, dimension_value = (
                condition
            )

            if (
                not isinstance(
                    dimension_type,
                    str,
                )
                or not dimension_type.strip()
            ):
                raise ValueError(
                    "condition dimension_type "
                    "must not be empty"
                )

            if (
                not isinstance(
                    dimension_value,
                    str,
                )
                or not dimension_value.strip()
            ):
                raise ValueError(
                    "condition dimension_value "
                    "must not be empty"
                )

            if (
                dimension_type
                not in (
                    self.context_definition.dimension_types
                )
            ):
                raise ValueError(
                    "undeclared condition "
                    "dimension_type: "
                    f"{dimension_type}"
                )

            if (
                dimension_type
                in seen_dimension_types
            ):
                raise ValueError(
                    "duplicate condition "
                    "dimension_type: "
                    f"{dimension_type}"
                )

            seen_dimension_types.add(
                dimension_type,
            )

        if not isinstance(
            self.source_policy_ids,
            tuple,
        ):
            raise TypeError(
                "source_policy_ids "
                "must be an immutable tuple"
            )

        seen_policy_ids: set[str] = set()

        for policy_id in (
            self.source_policy_ids
        ):
            if (
                not isinstance(
                    policy_id,
                    str,
                )
                or not policy_id.strip()
            ):
                raise ValueError(
                    "source policy_id "
                    "must not be empty"
                )

            if policy_id in seen_policy_ids:
                raise ValueError(
                    "duplicate source policy_id: "
                    f"{policy_id}"
                )

            seen_policy_ids.add(
                policy_id,
            )
