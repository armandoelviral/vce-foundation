from phase3.historical_governance_replay.historical_governance_snapshot import (
    HistoricalGovernanceSnapshot,
)


class HistoricalReplayEvaluation:

    @staticmethod
    def evaluate(
        snapshot: HistoricalGovernanceSnapshot,
    ) -> bool:

        if not snapshot.policy_version:
            return False

        if not snapshot.authority_id:
            return False

        return True
