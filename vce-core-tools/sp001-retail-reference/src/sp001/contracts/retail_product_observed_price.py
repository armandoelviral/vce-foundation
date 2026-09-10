from dataclasses import dataclass

from sp001.contracts.retail_commercial_monetary_amount import (
    RetailCommercialMonetaryAmount,
)
from sp001.contracts.retail_context_observation_provenance_binding import (
    RetailContextObservationProvenanceBinding,
)
from sp001.contracts.retail_context_scope import RetailContextScope
from sp001.contracts.retail_product_identity import RetailProductIdentity


@dataclass(frozen=True, slots=True)
class RetailProductObservedPrice:
    """Immutable exact product price observed in one retail context."""

    product_identity: RetailProductIdentity
    context_scope: RetailContextScope
    monetary_amount: RetailCommercialMonetaryAmount
    pricing_scheme_id: str
    pricing_scheme_version: int
    provenance_binding: RetailContextObservationProvenanceBinding

    def __post_init__(self) -> None:
        if not isinstance(
            self.product_identity,
            RetailProductIdentity,
        ):
            raise TypeError(
                "product_identity must be a RetailProductIdentity"
            )

        if not isinstance(self.context_scope, RetailContextScope):
            raise TypeError(
                "context_scope must be a RetailContextScope"
            )

        if not isinstance(
            self.monetary_amount,
            RetailCommercialMonetaryAmount,
        ):
            raise TypeError(
                "monetary_amount must be a "
                "RetailCommercialMonetaryAmount"
            )

        if self.monetary_amount.minor_unit_amount < 0:
            raise ValueError(
                "monetary_amount must not be negative"
            )

        if not isinstance(self.pricing_scheme_id, str):
            raise TypeError("pricing_scheme_id must be a string")

        if not self.pricing_scheme_id:
            raise ValueError("pricing_scheme_id must not be empty")

        if (
            isinstance(self.pricing_scheme_version, bool)
            or not isinstance(self.pricing_scheme_version, int)
        ):
            raise TypeError(
                "pricing_scheme_version must be an integer"
            )

        if self.pricing_scheme_version <= 0:
            raise ValueError(
                "pricing_scheme_version must be positive"
            )

        if not isinstance(
            self.provenance_binding,
            RetailContextObservationProvenanceBinding,
        ):
            raise TypeError(
                "provenance_binding must be a "
                "RetailContextObservationProvenanceBinding"
            )

        if (
            self.provenance_binding.snapshot.context_scope
            != self.context_scope
        ):
            raise ValueError(
                "context_scope must match the context scope "
                "referenced by provenance_binding snapshot"
            )
