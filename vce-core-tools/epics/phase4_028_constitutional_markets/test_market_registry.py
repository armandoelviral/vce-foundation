from epics.phase4_028_constitutional_markets.market_offer import (
    MarketOffer,
)
from epics.phase4_028_constitutional_markets.market_registry import (
    MarketRegistry,
)


def test_registry_stores_offer():
    registry = MarketRegistry()

    offer = MarketOffer(
        offer_id="offer.001",
        seller_id="institution.alpha",
        asset_type="delegation_capacity",
        quantity=50,
        requested_value=100,
    )

    registry.add(offer)

    assert registry.offers() == [offer]


def test_registry_rejects_duplicate_offer():
    registry = MarketRegistry()

    offer = MarketOffer(
        offer_id="offer.001",
        seller_id="institution.alpha",
        asset_type="delegation_capacity",
        quantity=50,
        requested_value=100,
    )

    registry.add(offer)

    try:
        registry.add(offer)
        assert False
    except ValueError as exc:
        assert "duplicate offer" in str(exc)


def test_registry_returns_copy():
    registry = MarketRegistry()

    offer = MarketOffer(
        offer_id="offer.001",
        seller_id="institution.alpha",
        asset_type="delegation_capacity",
        quantity=50,
        requested_value=100,
    )

    registry.add(offer)

    offers = registry.offers()
    offers.clear()

    assert len(registry.offers()) == 1
