from epics.phase4_028_constitutional_markets.market_matching import (
    match_offer,
)
from epics.phase4_028_constitutional_markets.market_offer import (
    MarketOffer,
)


def test_matching_offer():
    offer = MarketOffer(
        offer_id="offer.001",
        seller_id="institution.alpha",
        asset_type="delegation_capacity",
        quantity=50,
        requested_value=100,
    )

    result = match_offer(
        offer=offer,
        requested_asset_type="delegation_capacity",
        offered_value=100,
    )

    assert result["matched"] is True


def test_asset_type_mismatch():
    offer = MarketOffer(
        offer_id="offer.001",
        seller_id="institution.alpha",
        asset_type="delegation_capacity",
        quantity=50,
        requested_value=100,
    )

    result = match_offer(
        offer=offer,
        requested_asset_type="other_asset",
        offered_value=100,
    )

    assert result["matched"] is False


def test_value_too_low():
    offer = MarketOffer(
        offer_id="offer.001",
        seller_id="institution.alpha",
        asset_type="delegation_capacity",
        quantity=50,
        requested_value=100,
    )

    result = match_offer(
        offer=offer,
        requested_asset_type="delegation_capacity",
        offered_value=99,
    )

    assert result["matched"] is False
