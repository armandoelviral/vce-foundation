from dataclasses import dataclass


@dataclass(frozen=True)
class RegionScopedLedgerKey:
    region: str
    artifact_hash: str
    ledger_sequence: int

    def build_key(self):

        return (
            f"region={self.region}/"
            f"sequence={self.ledger_sequence}/"
            f"artifact={self.artifact_hash}.json"
        )
