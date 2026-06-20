from phase4.hot_consensus_cold_proof.proof_job_record import (
    ProofJobRecord,
)

from phase4.hot_consensus_cold_proof.proof_job_queue import (
    ProofJobQueue,
)

from phase4.hot_consensus_cold_proof.async_prover_dispatch import (
    AsyncProverDispatch,
)

from phase4.hot_consensus_cold_proof.proof_result_record import (
    ProofResultRecord,
)

from phase4.hot_consensus_cold_proof.proof_attachment import (
    ProofAttachment,
)

from phase4.hot_consensus_cold_proof.transparency_proof_anchor import (
    TransparencyProofAnchor,
)

from phase4.hot_consensus_cold_proof.browser_proof_verification import (
    BrowserProofVerification,
)


def test_end_to_end_hot_consensus_cold_proof():

    job = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="SP1",
        status="PENDING",
    )

    queue = ProofJobQueue()

    queue.enqueue(job)

    dispatcher = AsyncProverDispatch(
        queue
    )

    dispatched = dispatcher.dispatch()

    assert dispatched == job

    result = ProofResultRecord(
        result_id="result-001",
        job_id=dispatched.job_id,
        proof_hash="proof-hash-001",
        status="COMPLETED",
    )

    attachment = ProofAttachment.attach(
        execution_request_id=(
            dispatched.execution_request_id
        ),
        proof_result=result,
    )

    anchor = TransparencyProofAnchor.anchor(
        anchor_id="anchor-001",
        attachment=attachment,
    )

    assert (
        BrowserProofVerification.verify(
            anchor
        )
        is True
    )
