from epics.phase4_028_constitutional_markets.market_offer import (
    MarketOffer,
)


class MarketRegistry:
    def __init__(self):
        self._offers = []
        self._offer_ids = set()

    def add(self, offer: MarketOffer):
        if offer.offer_id in self._offer_ids:
            raise ValueError("duplicate offer")

        self._offers.append(offer)
        self._offer_ids.add(offer.offer_id)

    def offers(self):
        return list(self._offers)
