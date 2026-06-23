from epics.phase4_028_constitutional_markets.market_offer import (
    MarketOffer,
)


def test_market_offer_creation():
    offer = MarketOffer(
        offer_id="offer.001",
        seller_id="institution.alpha",
        asset_type="delegation_capacity",
        quantity=50,
        requested_value=100,
    )

    assert offer.offer_id == "offer.001"
    assert offer.seller_id == "institution.alpha"
    assert offer.asset_type == "delegation_capacity"
    assert offer.quantity == 50
    assert offer.requested_value == 100


def test_rejects_empty_offer_id():
    try:
        MarketOffer(
            offer_id="",
            seller_id="institution.alpha",
            asset_type="delegation_capacity",
            quantity=50,
            requested_value=100,
        )
        assert False
    except ValueError as exc:
        assert "offer_id" in str(exc)


def test_rejects_non_positive_quantity():
    try:
        MarketOffer(
            offer_id="offer.001",
            seller_id="institution.alpha",
            asset_type="delegation_capacity",
            quantity=0,
            requested_value=100,
        )
        assert False
    except ValueError as exc:
        assert "quantity" in str(exc)
