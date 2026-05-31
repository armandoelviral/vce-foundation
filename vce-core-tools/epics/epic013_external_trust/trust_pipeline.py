from epics.epic012_replay_runtime.runtime_core import RuntimeCore
from epics.epic012_replay_runtime.attestation import ExecutionAttestation
from epics.epic012_replay_runtime.signed_attestation import SignedAttestation
from epics.epic013_external_trust.external_trust_engine import ExternalTrustEngine


class RuntimeExternalTrustPipeline:

    def __init__(self):
        self.runtime = RuntimeCore()
        self.attestation_builder = ExecutionAttestation()
        self.signer = SignedAttestation()
        self.external_trust = ExternalTrustEngine()

    def execute(self, events, certificate):
        state = self.runtime.execute(events)

        attestation = self.attestation_builder.build(
            events,
            state
        )

        signed_attestation = self.signer.sign(
            attestation
        )

        signature_valid = self.signer.verify(
            signed_attestation
        )

        if not signature_valid:
            return {
                "runtime_replay": "VERIFIED",
                "attestation_signature": "INVALID",
                "external_trust": "REJECTED",
                "ledger_admission": "DENIED",
            }

        trusted = self.external_trust.verify(
            certificate,
            signed_attestation
        )

        return {
            "runtime_replay": "VERIFIED",
            "attestation_signature": "VALID",
            "external_trust": "ACCEPTED" if trusted else "REJECTED",
            "ledger_admission": "APPROVED" if trusted else "DENIED",
            "state_hash": state.state_hash,
            "sequence_number": state.sequence_number,
        }
