from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)


class ReplayEvidenceBundle:

    def __init__(self):

        self._records = []

    def add(
        self,
        record: ReplayEvidenceRecord,
    ) -> None:

        self._records.append(
            record
        )

    def records(
        self,
    ):

        return list(
            self._records
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )

    def to_dict(
        self,
    ):

        return {
            "count": self.count(),
            "records": [
                record.to_dict()
                for record in self._records
            ],
        }
