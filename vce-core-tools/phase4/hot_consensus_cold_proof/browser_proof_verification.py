from phase4.hot_consensus_cold_proof.transparency_proof_anchor import (
    TransparencyProofAnchor,
)


class BrowserProofVerification:

    @staticmethod
    def verify(
        anchor: TransparencyProofAnchor,
    ) -> bool:

        if not anchor.anchor_id:
            return False

        if not anchor.execution_request_id:
            return False

        if not anchor.result_id:
            return False

        if not anchor.proof_hash:
            return False

        return True
