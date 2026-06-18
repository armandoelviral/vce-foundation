from phase3.replay_evidence_bundle.replay_evidence_bundle import (
    ReplayEvidenceBundle,
)


class BundleBuilder:

    @staticmethod
    def build(
        records,
    ) -> ReplayEvidenceBundle:

        bundle = ReplayEvidenceBundle()

        for record in records:

            bundle.add(
                record
            )

        return bundle
