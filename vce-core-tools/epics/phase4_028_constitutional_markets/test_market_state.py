from epics.phase4_028_constitutional_markets.market_settlement import (
    MarketSettlementRecord,
)
from epics.phase4_028_constitutional_markets.market_state import (
    MarketState,
)


def test_builds_market_state():
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

    state = MarketState.from_settlements(settlements)

    assert state.settlement_count == 2
    assert state.total_settled_value == 160
    assert state.total_quantity == 75


def test_empty_market_state():
    state = MarketState.from_settlements([])

    assert state.settlement_count == 0
    assert state.total_settled_value == 0
    assert state.total_quantity == 0


def test_state_is_immutable_snapshot():
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

    state = MarketState.from_settlements(settlements)

    settlements.append(
        MarketSettlementRecord(
            settlement_id="settlement.002",
            offer_id="offer.002",
            buyer_id="citizen.gamma",
            seller_id="institution.alpha",
            asset_type="delegation_capacity",
            quantity=25,
            settled_value=60,
        )
    )

    assert state.settlement_count == 1
    assert state.total_settled_value == 100
    assert state.total_quantity == 50
