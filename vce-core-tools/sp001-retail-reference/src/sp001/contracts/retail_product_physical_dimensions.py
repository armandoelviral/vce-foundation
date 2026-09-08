from dataclasses import dataclass

from sp001.contracts.retail_product_identity import (
    RetailProductIdentity,
)


@dataclass(frozen=True, slots=True)
class RetailProductPhysicalDimensions:
    """Declared product dimensions in canonical integer millimeters."""

    product_identity: RetailProductIdentity
    height_millimeters: int
    width_millimeters: int
    depth_millimeters: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.product_identity,
            RetailProductIdentity,
        ):
            raise TypeError(
                "product_identity must be a RetailProductIdentity"
            )

        measurements = {
            "height_millimeters": self.height_millimeters,
            "width_millimeters": self.width_millimeters,
            "depth_millimeters": self.depth_millimeters,
        }

        for field, measurement in measurements.items():
            if (
                isinstance(
                    measurement,
                    bool,
                )
                or not isinstance(
                    measurement,
                    int,
                )
                or measurement < 1
            ):
                raise ValueError(
                    f"{field} must be a positive integer"
                )
