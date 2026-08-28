from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetailProcessRole:
    """Immutable customer-scoped organizational role identity."""

    role_id: str
    customer_id: str
    role_name: str

    def __post_init__(self) -> None:
        identity_fields = {
            "role_id": self.role_id,
            "customer_id": self.customer_id,
            "role_name": self.role_name,
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
