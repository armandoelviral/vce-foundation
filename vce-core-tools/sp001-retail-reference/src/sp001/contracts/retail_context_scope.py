from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetailContextScope:
    """Immutable customer-declared retail operating context identity."""

    context_id: str
    commercial_channel_id: str
    point_of_sale_id: str
    department_id: str
    profile_version: int

    def __post_init__(self) -> None:
        identity_fields = {
            "context_id": self.context_id,
            "commercial_channel_id": self.commercial_channel_id,
            "point_of_sale_id": self.point_of_sale_id,
            "department_id": self.department_id,
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
                self.profile_version,
                bool,
            )
            or not isinstance(
                self.profile_version,
                int,
            )
            or self.profile_version < 1
        ):
            raise ValueError(
                "profile_version must be a positive integer"
            )
