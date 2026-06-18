from phase3.replay_evidence_bundle.replay_evidence_bundle import (
    ReplayEvidenceBundle,
)


class ReplayAuditor:

    @staticmethod
    def audit(
        bundle: ReplayEvidenceBundle,
    ) -> bool:

        if bundle is None:
            return False

        return bundle.count() > 0
