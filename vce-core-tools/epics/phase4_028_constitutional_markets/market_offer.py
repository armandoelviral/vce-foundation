from dataclasses import dataclass


@dataclass(frozen=True)
class MarketOffer:
    offer_id: str
    seller_id: str
    asset_type: str
    quantity: int
    requested_value: int

    def __post_init__(self):
        if not self.offer_id:
            raise ValueError("offer_id is required")

        if not self.seller_id:
            raise ValueError("seller_id is required")

        if not self.asset_type:
            raise ValueError("asset_type is required")

        if self.quantity <= 0:
            raise ValueError("quantity must be positive")

        if self.requested_value <= 0:
            raise ValueError("requested_value must be positive")
