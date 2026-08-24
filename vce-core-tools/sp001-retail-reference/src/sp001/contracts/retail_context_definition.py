from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetailContextDefinition:
    """Immutable customer-declared configuration of retail context dimensions."""

    context_definition_id: str
    customer_id: str
    definition_version: int
    dimension_types: tuple[str, ...]
    required_dimension_types: tuple[str, ...] = ()
    optional_dimension_types: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        identity_fields = {
            "context_definition_id": self.context_definition_id,
            "customer_id": self.customer_id,
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
                self.definition_version,
                bool,
            )
            or not isinstance(
                self.definition_version,
                int,
            )
            or self.definition_version < 1
        ):
            raise ValueError(
                "definition_version must be a positive integer"
            )

        if not isinstance(
            self.dimension_types,
            tuple,
        ):
            raise TypeError(
                "dimension_types must be an immutable tuple"
            )

        if not self.dimension_types:
            raise ValueError(
                "dimension_types must not be empty"
            )

        seen_dimension_types: set[str] = set()

        for dimension_type in self.dimension_types:
            if (
                not isinstance(
                    dimension_type,
                    str,
                )
                or not dimension_type.strip()
            ):
                raise ValueError(
                    "dimension_type must not be empty"
                )

            if dimension_type in seen_dimension_types:
                raise ValueError(
                    "duplicate dimension_type: "
                    f"{dimension_type}"
                )

            seen_dimension_types.add(
                dimension_type,
            )

        requirement_collections = (
            (
                "required",
                self.required_dimension_types,
            ),
            (
                "optional",
                self.optional_dimension_types,
            ),
        )

        for requirement_name, requirement_types in (
            requirement_collections
        ):
            if not isinstance(
                requirement_types,
                tuple,
            ):
                raise TypeError(
                    f"{requirement_name}_dimension_types "
                    "must be an immutable tuple"
                )

            seen_requirement_types: set[str] = set()

            for dimension_type in requirement_types:
                if (
                    not isinstance(
                        dimension_type,
                        str,
                    )
                    or not dimension_type.strip()
                ):
                    raise ValueError(
                        f"{requirement_name} dimension_type "
                        "must not be empty"
                    )

                if dimension_type in seen_requirement_types:
                    raise ValueError(
                        f"duplicate {requirement_name} "
                        "dimension_type: "
                        f"{dimension_type}"
                    )

                if dimension_type not in seen_dimension_types:
                    raise ValueError(
                        f"undeclared {requirement_name} "
                        "dimension_type: "
                        f"{dimension_type}"
                    )

                seen_requirement_types.add(
                    dimension_type,
                )

        required_types = set(
            self.required_dimension_types,
        )
        optional_types = set(
            self.optional_dimension_types,
        )

        for dimension_type in self.dimension_types:
            if (
                dimension_type in required_types
                and dimension_type in optional_types
            ):
                raise ValueError(
                    "dimension_type cannot be both required "
                    "and optional: "
                    f"{dimension_type}"
                )

        if required_types or optional_types:
            classified_types = (
                required_types
                | optional_types
            )

            for dimension_type in self.dimension_types:
                if dimension_type not in classified_types:
                    raise ValueError(
                        "dimension requirements must classify "
                        "every dimension_type: "
                        f"{dimension_type}"
                    )
