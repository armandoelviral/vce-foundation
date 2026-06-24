from dataclasses import dataclass


@dataclass(frozen=True)
class RealityLedgerRecord:
    ledger_id: str
    claim_id: str
    consensus_id: str

    def __post_init__(self):
        if not self.ledger_id:
            raise ValueError("ledger_id is required")

        if not self.claim_id:
            raise ValueError("claim_id is required")

        if not self.consensus_id:
            raise ValueError("consensus_id is required")
