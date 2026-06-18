from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)

from phase2.attestation_persistence.state_attestation import (
    StateAttestation,
)


def test_attests_runtime_state():

    state = RuntimeState(
        events_applied=2,
        last_lsn=2,
        state_hash="state-hash-001",
    )

    record = StateAttestation.attest(
        attestation_id="att-001",
        state=state,
    )

    assert record.subject == "runtime-state"


def test_state_attestation_uses_state_hash():

    state = RuntimeState(
        events_applied=2,
        last_lsn=2,
        state_hash="state-hash-001",
    )

    record = StateAttestation.attest(
        attestation_id="att-001",
        state=state,
    )

    assert record.evidence_hash == "state-hash-001"


def test_state_attestation_preserves_id():

    state = RuntimeState(
        events_applied=2,
        last_lsn=2,
        state_hash="state-hash-001",
    )

    record = StateAttestation.attest(
        attestation_id="att-001",
        state=state,
    )

    assert record.attestation_id == "att-001"
