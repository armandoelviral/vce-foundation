class EvidenceAttributeRecovery:

    def __init__(
        self,
        evidence_ledger,
    ):

        self._evidence_ledger = evidence_ledger

    def recover(
        self,
        evidence_hash,
    ):

        return self._evidence_ledger.get(
            evidence_hash
        )
