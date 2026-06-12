from dataclasses import dataclass


@dataclass(frozen=True)
class ConsensusAttestation:
    ledger_root_hash: str
    policy: str
    observed_votes: int
    total_votes: int
    consensus: str

    def to_dict(self):

        return {
            "ledger_root_hash": self.ledger_root_hash,
            "policy": self.policy,
            "observed_votes": self.observed_votes,
            "total_votes": self.total_votes,
            "consensus": self.consensus,
        }


def build_consensus_attestation(
    ledger_root_hash,
    evaluation,
):

    return ConsensusAttestation(
        ledger_root_hash=ledger_root_hash,
        policy=evaluation["policy"],
        observed_votes=evaluation["observed_votes"],
        total_votes=evaluation["total_votes"],
        consensus=evaluation["consensus"],
    )
