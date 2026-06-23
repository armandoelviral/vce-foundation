from epics.phase4_028_constitutional_markets.market_matching import (
    match_offer,
)
from epics.phase4_028_constitutional_markets.market_offer import (
    MarketOffer,
)
from epics.phase4_028_constitutional_markets.market_registry import (
    MarketRegistry,
)
from epics.phase4_028_constitutional_markets.market_settlement import (
    MarketSettlementRecord,
)
from epics.phase4_028_constitutional_markets.market_state import (
    MarketState,
)
from epics.phase4_028_constitutional_markets.market_verifier import (
    verify_market_state,
)


def test_end_to_end_constitutional_market_flow():
    registry = MarketRegistry()

    offer = MarketOffer(
        offer_id="offer.001",
        seller_id="institution.alpha",
        asset_type="delegation_capacity",
        quantity=50,
        requested_value=100,
    )

    registry.add(offer)

    match = match_offer(
        offer=offer,
        requested_asset_type="delegation_capacity",
        offered_value=100,
    )

    assert match["matched"] is True

    settlement = MarketSettlementRecord(
        settlement_id="settlement.001",
        offer_id=offer.offer_id,
        buyer_id="citizen.beta",
        seller_id=offer.seller_id,
        asset_type=offer.asset_type,
        quantity=offer.quantity,
        settled_value=100,
    )

    state = MarketState.from_settlements(
        [settlement]
    )

    assert state.settlement_count == 1
    assert state.total_quantity == 50
    assert state.total_settled_value == 100

    verification = verify_market_state(state)

    assert verification["verified"] is True
