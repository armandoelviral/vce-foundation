from phase3.governance_execution_engine.execution_request_record import (
    ExecutionRequestRecord,
)

from phase3.governance_execution_engine.execution_attestation import (
    ExecutionAttestation,
)


def test_attestation_subject():

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    attestation = (
        ExecutionAttestation.attest(
            attestation_id="att-001",
            request=request,
        )
    )

    assert (
        attestation.subject
        == "governance_execution"
    )


def test_attestation_uses_request_id():

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    attestation = (
        ExecutionAttestation.attest(
            attestation_id="att-001",
            request=request,
        )
    )

    assert (
        attestation.evidence_hash
        == "request-001"
    )


def test_attestation_preserves_id():

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    attestation = (
        ExecutionAttestation.attest(
            attestation_id="att-001",
            request=request,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
