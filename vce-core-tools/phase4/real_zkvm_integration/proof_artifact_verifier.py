from phase4.real_zkvm_integration.proof_artifact_record import (
    ProofArtifactRecord,
)


class ProofArtifactVerifier:

    @staticmethod
    def verify(
        artifact: ProofArtifactRecord,
    ) -> bool:

        if not artifact.artifact_id:
            return False

        if not artifact.execution_request_id:
            return False

        if not artifact.prover_type:
            return False

        if not artifact.proof_hash:
            return False

        return True
