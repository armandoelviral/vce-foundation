from phase4.real_zkvm_integration.sp1_prover_adapter import (
    SP1ProverAdapter,
)

from phase4.real_zkvm_integration.proof_artifact_record import (
    ProofArtifactRecord,
)

from phase4.real_zkvm_integration.proof_artifact_verifier import (
    ProofArtifactVerifier,
)

from phase4.real_zkvm_integration.d5_zk_proof_attachment import (
    D5zkProofAttachment,
)

from phase4.real_zkvm_integration.d7_browser_zk_verification import (
    D7BrowserZkVerification,
)


def test_end_to_end_real_zk_proof():

    adapter = SP1ProverAdapter()

    proof = adapter.generate_proof(
        execution_request_id="request-001"
    )

    artifact = ProofArtifactRecord(
        artifact_id="artifact-001",
        execution_request_id=proof[
            "execution_request_id"
        ],
        prover_type=proof[
            "prover_type"
        ],
        proof_hash=proof[
            "proof_hash"
        ],
        verification_status="UNVERIFIED",
    )

    assert (
        ProofArtifactVerifier.verify(
            artifact
        )
        is True
    )

    attachment = (
        D5zkProofAttachment.attach(
            d5_artifact_id="d5-001",
            proof_artifact=artifact,
        )
    )

    assert (
        D7BrowserZkVerification.verify(
            attachment
        )
        is True
    )
