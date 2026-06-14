from epics.ztc12_browser_verification_portal.browser_replay_verifier import (
    BrowserReplayVerifier,
)


def test_accepts_matching_state_root():

    assert BrowserReplayVerifier.verify(
        historical_state_root="root-001",
        recomputed_state_root="root-001",
    )


def test_rejects_mismatched_state_root():

    assert not BrowserReplayVerifier.verify(
        historical_state_root="root-001",
        recomputed_state_root="root-002",
    )


def test_rejects_missing_historical_state_root():

    assert not BrowserReplayVerifier.verify(
        historical_state_root="",
        recomputed_state_root="root-001",
    )


def test_rejects_missing_recomputed_state_root():

    assert not BrowserReplayVerifier.verify(
        historical_state_root="root-001",
        recomputed_state_root="",
    )
