from epics.phase4_028_constitutional_markets.market_offer import (
    MarketOffer,
)


def match_offer(
    offer: MarketOffer,
    requested_asset_type: str,
    offered_value: int,
):
    return {
        "matched": (
            offer.asset_type == requested_asset_type
            and offered_value >= offer.requested_value
        ),
        "offer_id": offer.offer_id,
    }
