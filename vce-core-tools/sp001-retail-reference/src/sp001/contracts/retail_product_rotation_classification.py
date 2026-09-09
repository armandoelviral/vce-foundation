from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_product_identity import (
    RetailProductIdentity,
)


class RetailProductRotationClass(StrEnum):
    """Closed declared product rotation category without derived meaning."""

    A = "A"
    B = "B"
    C = "C"


@dataclass(frozen=True, slots=True)
class RetailProductDeclaredRotationClassification:
    """Product rotation class under one explicit versioned scheme."""

    product_identity: RetailProductIdentity
    rotation_class: RetailProductRotationClass
    classification_scheme_id: str
    classification_scheme_version: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.product_identity,
            RetailProductIdentity,
        ):
            raise TypeError(
                "product_identity must be a RetailProductIdentity"
            )

        if not isinstance(
            self.rotation_class,
            RetailProductRotationClass,
        ):
            raise TypeError(
                "rotation_class must be a RetailProductRotationClass"
            )

        if (
            not isinstance(
                self.classification_scheme_id,
                str,
            )
            or not self.classification_scheme_id.strip()
        ):
            raise ValueError(
                "classification_scheme_id must not be empty"
            )

        if (
            isinstance(
                self.classification_scheme_version,
                bool,
            )
            or not isinstance(
                self.classification_scheme_version,
                int,
            )
            or self.classification_scheme_version < 1
        ):
            raise ValueError(
                "classification_scheme_version must be "
                "a positive integer"
            )
