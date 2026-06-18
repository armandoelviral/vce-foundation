
from phase3.replay_evidence_bundle.replay_evidence_bundle import (
    ReplayEvidenceBundle,
)


class BundleQuery:

    def __init__(
        self,
        bundle: ReplayEvidenceBundle,
    ):

        self.bundle = bundle

    def by_id(
        self,
        evidence_id: str,
    ):

        for record in self.bundle.records():

            if (
                record.evidence_id
                == evidence_id
            ):
                return record

        return None
