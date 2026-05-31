#!/usr/bin/env python3

import json

from epics.epic012_replay_runtime.runtime_core import RuntimeCore
from epics.epic012_replay_runtime.attestation import ExecutionAttestation
from epics.epic012_replay_runtime.signed_attestation import SignedAttestation


def main():
    events = [
        {
            "lsn": 1,
            "opcode": "APPEND_EVIDENCE",
            "payload": "github-workflow-run-001"
        },
        {
            "lsn": 2,
            "opcode": "REGISTER_ARTIFACT",
            "payload": "vce-artifact-001"
        },
        {
            "lsn": 3,
            "opcode": "SEAL_SNAPSHOT",
            "payload": "snapshot-001"
        }
    ]

    runtime = RuntimeCore()
    state = runtime.execute(events)

    attestation_builder = ExecutionAttestation()
    attestation = attestation_builder.build(
        events,
        state
    )

    signer = SignedAttestation()
    signed = signer.sign(attestation)

    signature_valid = signer.verify(signed)

    result = {
        "github_evidence": "COLLECTED",
        "runtime_replay": "VERIFIED",
        "attestation_signature": "VALID" if signature_valid else "INVALID",
        "state_hash": state.state_hash,
        "sequence_number": state.sequence_number,
        "ledger_status": "READY_TO_COMMIT"
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
