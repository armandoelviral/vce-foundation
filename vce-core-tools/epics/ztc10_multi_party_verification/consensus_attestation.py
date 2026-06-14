from typing import Iterable

from epics.ztc10_multi_party_verification.witness_response import (
    WitnessResponse,
)


class ConsensusAttestation:

    @staticmethod
    def build(
        winning_state_root: str,
        quorum_policy: str,
        witnesses: Iterable[WitnessResponse],
    ) -> dict:

        return {
            "winning_state_root": winning_state_root,
            "quorum_policy": quorum_policy,
            "consensus_verified": True,
            "witnesses": [
                {
                    "witness_id": witness.witness_id,
                    "state_root_hash": witness.state_root_hash,
                    "classical_signature": witness.classical_signature,
                    "pqc_signature": witness.pqc_signature,
                    "accepted": witness.accepted,
                }
                for witness in witnesses
            ],
        }
