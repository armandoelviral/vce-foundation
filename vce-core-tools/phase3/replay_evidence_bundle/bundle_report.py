from phase3.replay_evidence_bundle.replay_evidence_bundle import (
    ReplayEvidenceBundle,
)


class BundleReport:

    def __init__(
        self,
        bundle: ReplayEvidenceBundle,
    ):

        self.bundle = bundle

    def record_count(
        self,
    ) -> int:

        return self.bundle.count()

    def evidence_ids(
        self,
    ):

        return [
            record.evidence_id
            for record in self.bundle.records()
        ]

    def to_dict(
        self,
    ):

        return {
            "record_count":
                self.record_count(),
            "evidence_ids":
                self.evidence_ids(),
        }
