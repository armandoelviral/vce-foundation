from epics.epic013_external_trust.trust_pipeline import RuntimeExternalTrustPipeline
from epics.epic013_external_trust.ledger_admission import LedgerAdmissionController


class FullTrustPipeline:

    def __init__(self):

        self.trust_pipeline = RuntimeExternalTrustPipeline()
        self.ledger = LedgerAdmissionController()


    def execute(self, events, certificate):

        trust_result = self.trust_pipeline.execute(
            events,
            certificate
        )

        ledger_result = self.ledger.admit(
            trust_result
        )

        return {
            "trust": trust_result,
            "ledger": ledger_result
        }
