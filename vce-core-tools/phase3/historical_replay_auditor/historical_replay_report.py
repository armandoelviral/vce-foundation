from phase3.historical_replay_auditor.replay_certification import (
    ReplayCertification,
)


class HistoricalReplayReport:

    def __init__(
        self,
        certification: ReplayCertification,
    ):

        self.certification = certification

    def status(
        self,
    ) -> str:

        return self.certification.status

    def certified(
        self,
    ) -> bool:

        return self.certification.certified

    def to_dict(
        self,
    ):

        return {
            "status":
                self.status(),
            "certified":
                self.certified(),
        }
