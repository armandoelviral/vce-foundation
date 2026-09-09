from dataclasses import dataclass

from sp001.contracts.retail_product_identity import (
    RetailProductIdentity,
)


@dataclass(frozen=True, slots=True)
class RetailProductDeclaredSubstitute:
    """Immutable declared substitution edge between two retail products."""

    product_identity: RetailProductIdentity
    substitute_product_identity: RetailProductIdentity
    substitution_scheme_id: str
    substitution_scheme_version: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.product_identity,
            RetailProductIdentity,
        ):
            raise TypeError(
                "product_identity must be a RetailProductIdentity"
            )

        if not isinstance(
            self.substitute_product_identity,
            RetailProductIdentity,
        ):
            raise TypeError(
                "substitute_product_identity must be a "
                "RetailProductIdentity"
            )

        if (
            not isinstance(
                self.substitution_scheme_id,
                str,
            )
            or not self.substitution_scheme_id.strip()
        ):
            raise ValueError(
                "substitution_scheme_id must not be empty"
            )

        if (
            isinstance(
                self.substitution_scheme_version,
                bool,
            )
            or not isinstance(
                self.substitution_scheme_version,
                int,
            )
            or self.substitution_scheme_version < 1
        ):
            raise ValueError(
                "substitution_scheme_version must be a "
                "positive integer"
            )

        if (
            self.product_identity
            == self.substitute_product_identity
        ):
            raise ValueError(
                "a product cannot substitute itself"
            )
