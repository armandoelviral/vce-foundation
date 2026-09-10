from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetailCommercialCurrencyIdentity:
    """Declared currency code within one explicitly versioned scheme."""

    currency_code: str
    currency_scheme_id: str
    currency_scheme_version: int

    def __post_init__(self) -> None:
        if not isinstance(self.currency_code, str):
            raise TypeError("currency_code must be a string")

        if not self.currency_code:
            raise ValueError("currency_code must not be empty")

        if not isinstance(self.currency_scheme_id, str):
            raise TypeError("currency_scheme_id must be a string")

        if not self.currency_scheme_id:
            raise ValueError("currency_scheme_id must not be empty")

        if (
            isinstance(self.currency_scheme_version, bool)
            or not isinstance(self.currency_scheme_version, int)
        ):
            raise TypeError(
                "currency_scheme_version must be an integer"
            )

        if self.currency_scheme_version <= 0:
            raise ValueError(
                "currency_scheme_version must be positive"
            )
