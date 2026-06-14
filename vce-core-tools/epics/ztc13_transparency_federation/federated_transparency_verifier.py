from epics.ztc13_transparency_federation.federated_transparency_proof import (
    FederatedTransparencyProof,
)


class FederatedTransparencyVerifier:

    @staticmethod
    def verify(
        proof: FederatedTransparencyProof,
    ) -> bool:

        return all(
            [
                proof.anchor_id,
                proof.source_registry,
                proof.target_registry,
            ]
        )
