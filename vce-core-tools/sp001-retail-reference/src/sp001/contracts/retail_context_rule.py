from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetailContextRule:
    """Immutable customer-defined retail rule and its context dependencies."""

    rule_id: str
    rule_type: str
    required_dimension_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            not isinstance(self.rule_id, str)
            or not self.rule_id.strip()
        ):
            raise ValueError(
                "rule_id must not be empty"
            )

        if (
            not isinstance(self.rule_type, str)
            or not self.rule_type.strip()
        ):
            raise ValueError(
                "rule_type must not be empty"
            )

        if not isinstance(
            self.required_dimension_ids,
            tuple,
        ):
            raise TypeError(
                "required_dimension_ids must be an immutable tuple"
            )

        if not self.required_dimension_ids:
            raise ValueError(
                "required_dimension_ids must not be empty"
            )

        seen_ids: set[str] = set()

        for dimension_id in self.required_dimension_ids:
            if (
                not isinstance(dimension_id, str)
                or not dimension_id.strip()
            ):
                raise ValueError(
                    "required dimension_id must not be empty"
                )

            if dimension_id in seen_ids:
                raise ValueError(
                    "duplicate required dimension_id: "
                    f"{dimension_id}"
                )

            seen_ids.add(
                dimension_id
            )
