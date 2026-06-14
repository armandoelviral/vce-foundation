from epics.ztc12_browser_verification_portal.browser_hash_verifier import (
    BrowserHashVerifier,
)


def test_hash_is_deterministic():

    hash_1 = BrowserHashVerifier.compute(
        "evidence-payload"
    )

    hash_2 = BrowserHashVerifier.compute(
        "evidence-payload"
    )

    assert hash_1 == hash_2


def test_accepts_matching_hash():

    payload = "evidence-payload"

    expected_hash = BrowserHashVerifier.compute(
        payload
    )

    assert BrowserHashVerifier.verify(
        payload,
        expected_hash,
    )


def test_rejects_mismatched_hash():

    assert not BrowserHashVerifier.verify(
        "evidence-payload",
        "wrong-hash",
    )
