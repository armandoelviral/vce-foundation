from epics.epic013_external_trust.full_trust_pipeline import FullTrustPipeline
from epics.epic013_external_trust.immutable_ledger import ImmutableLedgerStore


class ProvenanceEngine:

    def __init__(self):
        self.pipeline = FullTrustPipeline()
        self.ledger = ImmutableLedgerStore()

    def execute(self, events, certificate):

        result = self.pipeline.execute(
            events,
            certificate
        )

        trust_status = result["trust"]["external_trust"]
        ledger_status = result["ledger"]["status"]

        if ledger_status != "COMMITTED":
            return {
                "execution": "FAILED",
                "trust": trust_status,
                "ledger": ledger_status,
                "tamper_evident": False
            }

        self.ledger.append(
            {
                "state_hash": result["trust"]["state_hash"],
                "sequence_number": result["trust"]["sequence_number"],
                "external_trust": trust_status,
                "ledger_status": ledger_status
            }
        )

        return {
            "execution": result["trust"]["runtime_replay"],
            "trust": trust_status,
            "ledger": ledger_status,
            "tamper_evident": self.ledger.verify()
        }
