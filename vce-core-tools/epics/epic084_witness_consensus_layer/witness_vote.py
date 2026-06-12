from dataclasses import dataclass


@dataclass(frozen=True)
class WitnessVote:
    witness_id: str
    ledger_root_hash: str
    anchor_reference: str
    observed: bool
    observed_at: str

    def to_dict(self):

        return {
            "witness_id": self.witness_id,
            "ledger_root_hash": self.ledger_root_hash,
            "anchor_reference": self.anchor_reference,
            "observed": self.observed,
            "observed_at": self.observed_at,
        }
