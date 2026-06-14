from epics.ztc6_execution_provenance_binding.execution_provenance_record import (
    ExecutionProvenanceRecord,
)

from epics.ztc6_execution_provenance_binding.provenance_attestation import (
    ProvenanceAttestation,
)

from epics.ztc6_execution_provenance_binding.trusted_execution_gate import (
    TrustedExecutionGate,
)


def test_end_to_end_provenance_flow():

    record = ExecutionProvenanceRecord(
        artifact_hash="artifact-001",
        execution_id="execution-001",
        result_hash="result-001",
    )

    attestation = ProvenanceAttestation.build(
        record
    )

    trusted = TrustedExecutionGate.admit(
        attestation
    )

    assert trusted is True
