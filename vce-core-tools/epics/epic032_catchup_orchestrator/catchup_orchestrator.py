class CatchupOrchestrator:

    def __init__(self, ledger):
        self._ledger = ledger

    def catchup(self, canonical_events):
        self._ledger.replace_all(canonical_events)
