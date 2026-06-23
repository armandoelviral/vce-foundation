from dataclasses import dataclass


@dataclass(frozen=True)
class MarketSettlementRecord:
    settlement_id: str
    offer_id: str
    buyer_id: str
    seller_id: str
    asset_type: str
    quantity: int
    settled_value: int

    def __post_init__(self):
        if not self.settlement_id:
            raise ValueError("settlement_id is required")

        if not self.offer_id:
            raise ValueError("offer_id is required")

        if not self.buyer_id:
            raise ValueError("buyer_id is required")

        if not self.seller_id:
            raise ValueError("seller_id is required")

        if not self.asset_type:
            raise ValueError("asset_type is required")

        if self.quantity <= 0:
            raise ValueError("quantity must be positive")

        if self.settled_value <= 0:
            raise ValueError("settled_value must be positive")
