from phase3.replay_evidence_bundle.replay_evidence_bundle import (
    ReplayEvidenceBundle,
)


class BundleVerifier:

    @staticmethod
    def verify(
        bundle: ReplayEvidenceBundle,
    ) -> bool:

        if bundle.count() == 0:
            return False

        for record in bundle.records():

            if not record.evidence_id:
                return False

            if not record.evidence_type:
                return False

        return True
