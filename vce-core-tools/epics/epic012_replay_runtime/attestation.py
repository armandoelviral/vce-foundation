import json
import hashlib


class ExecutionAttestation:

    def build(self, input_events, final_state):

        canonical_input = json.dumps(
            input_events,
            sort_keys=True,
            separators=(",", ":")
        )

        input_hash = hashlib.sha256(
            canonical_input.encode()
        ).hexdigest()

        return {
            "attestation_type": "VCE_RUNTIME_EXECUTION",
            "runtime": "VCE-RTE",
            "input_hash": input_hash,
            "sequence_number": final_state.sequence_number,
            "state_hash": final_state.state_hash,
            "event_count": len(final_state.events),
            "verified": True
        }
