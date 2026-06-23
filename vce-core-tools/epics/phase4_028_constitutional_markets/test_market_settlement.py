from epics.phase4_028_constitutional_markets.market_settlement import (
    MarketSettlementRecord,
)


def test_market_settlement_record_creation():
    record = MarketSettlementRecord(
        settlement_id="settlement.001",
        offer_id="offer.001",
        buyer_id="citizen.beta",
        seller_id="institution.alpha",
        asset_type="delegation_capacity",
        quantity=50,
        settled_value=100,
    )

    assert record.settlement_id == "settlement.001"
    assert record.offer_id == "offer.001"
    assert record.buyer_id == "citizen.beta"
    assert record.seller_id == "institution.alpha"
    assert record.quantity == 50
    assert record.settled_value == 100


def test_rejects_empty_settlement_id():
    try:
        MarketSettlementRecord(
            settlement_id="",
            offer_id="offer.001",
            buyer_id="citizen.beta",
            seller_id="institution.alpha",
            asset_type="delegation_capacity",
            quantity=50,
            settled_value=100,
        )
        assert False
    except ValueError as exc:
        assert "settlement_id" in str(exc)


def test_rejects_non_positive_quantity():
    try:
        MarketSettlementRecord(
            settlement_id="settlement.001",
            offer_id="offer.001",
            buyer_id="citizen.beta",
            seller_id="institution.alpha",
            asset_type="delegation_capacity",
            quantity=0,
            settled_value=100,
        )
        assert False
    except ValueError as exc:
        assert "quantity" in str(exc)


def test_rejects_non_positive_settled_value():
    try:
        MarketSettlementRecord(
            settlement_id="settlement.001",
            offer_id="offer.001",
            buyer_id="citizen.beta",
            seller_id="institution.alpha",
            asset_type="delegation_capacity",
            quantity=50,
            settled_value=0,
        )
        assert False
    except ValueError as exc:
        assert "settled_value" in str(exc)
