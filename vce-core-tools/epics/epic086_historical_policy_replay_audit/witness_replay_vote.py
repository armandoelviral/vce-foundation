from dataclasses import dataclass


@dataclass(frozen=True)
class WitnessReplayVote:
    witness_id: str
    evidence_hash: str
    policy_id: str
    policy_version: str
    replay_result: str
    observed_at: str

    def to_dict(self):

        return {
            "witness_id": self.witness_id,
            "evidence_hash": self.evidence_hash,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "replay_result": self.replay_result,
            "observed_at": self.observed_at,
        }
