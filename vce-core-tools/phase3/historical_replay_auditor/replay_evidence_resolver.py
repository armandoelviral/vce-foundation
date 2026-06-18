from phase3.historical_replay_auditor.historical_replay_record import (
    HistoricalReplayRecord,
)


class ReplayEvidenceResolver:

    @staticmethod
    def resolve(
        replay: HistoricalReplayRecord,
        bundles,
    ):

        return bundles.get(
            replay.bundle_id
        )
