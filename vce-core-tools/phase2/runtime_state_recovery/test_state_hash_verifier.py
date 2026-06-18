from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)

from phase2.runtime_state_recovery.state_hash_verifier import (
    StateHashVerifier,
)


def test_accepts_matching_state_hash():

    state = RuntimeState(
        events_applied=2,
        last_lsn=2,
        state_hash="state-hash-001",
    )

    verifier = StateHashVerifier()

    assert verifier.verify(
        state=state,
        expected_hash="state-hash-001",
    )


def test_rejects_mismatched_state_hash():

    state = RuntimeState(
        events_applied=2,
        last_lsn=2,
        state_hash="state-hash-001",
    )

    verifier = StateHashVerifier()

    assert not verifier.verify(
        state=state,
        expected_hash="state-hash-999",
    )


def test_rejects_missing_expected_hash():

    state = RuntimeState(
        events_applied=2,
        last_lsn=2,
        state_hash="state-hash-001",
    )

    verifier = StateHashVerifier()

    assert not verifier.verify(
        state=state,
        expected_hash="",
    )
