from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)


class StateAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        state: RuntimeState,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="runtime-state",
            evidence_hash=state.state_hash,
        )
