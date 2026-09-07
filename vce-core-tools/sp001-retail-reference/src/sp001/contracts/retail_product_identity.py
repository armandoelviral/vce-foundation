from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetailProductIdentity:
    """Immutable product identity within one versioned retail catalog."""

    product_id: str
    sku: str
    catalog_id: str
    catalog_version: int

    def __post_init__(self) -> None:
        identity_fields = {
            "product_id": self.product_id,
            "sku": self.sku,
            "catalog_id": self.catalog_id,
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
                self.catalog_version,
                bool,
            )
            or not isinstance(
                self.catalog_version,
                int,
            )
            or self.catalog_version < 1
        ):
            raise ValueError(
                "catalog_version must be a positive integer"
            )
