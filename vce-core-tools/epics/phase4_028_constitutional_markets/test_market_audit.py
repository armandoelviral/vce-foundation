from epics.phase4_028_constitutional_markets.market_audit import (
    audit_market_settlements,
)
from epics.phase4_028_constitutional_markets.market_settlement import (
    MarketSettlementRecord,
)


def test_market_audit_returns_settlement_count_and_value():
    settlements = [
        MarketSettlementRecord(
            settlement_id="settlement.001",
            offer_id="offer.001",
            buyer_id="citizen.beta",
            seller_id="institution.alpha",
            asset_type="delegation_capacity",
            quantity=50,
            settled_value=100,
        ),
        MarketSettlementRecord(
            settlement_id="settlement.002",
            offer_id="offer.002",
            buyer_id="citizen.gamma",
            seller_id="institution.alpha",
            asset_type="delegation_capacity",
            quantity=25,
            settled_value=60,
        ),
    ]

    audit = audit_market_settlements(settlements)

    assert audit["settlement_count"] == 2
    assert audit["total_settled_value"] == 160
    assert audit["total_quantity"] == 75


def test_market_audit_empty_settlements():
    audit = audit_market_settlements([])

    assert audit["settlement_count"] == 0
    assert audit["total_settled_value"] == 0
    assert audit["total_quantity"] == 0
    assert audit["settlements"] == []


def test_market_audit_returns_copy():
    settlements = [
        MarketSettlementRecord(
            settlement_id="settlement.001",
            offer_id="offer.001",
            buyer_id="citizen.beta",
            seller_id="institution.alpha",
            asset_type="delegation_capacity",
            quantity=50,
            settled_value=100,
        )
    ]

    audit = audit_market_settlements(settlements)

    audit["settlements"].clear()

    assert len(settlements) == 1
