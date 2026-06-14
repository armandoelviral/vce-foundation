from epics.ztc12_browser_verification_portal.browser_transparency_verifier import (
    BrowserTransparencyVerifier,
)


def test_accepts_valid_anchor():

    assert BrowserTransparencyVerifier.verify(
        anchor_id="anchor-001",
        proof_present=True,
    )


def test_rejects_missing_proof():

    assert not BrowserTransparencyVerifier.verify(
        anchor_id="anchor-001",
        proof_present=False,
    )


def test_rejects_missing_anchor():

    assert not BrowserTransparencyVerifier.verify(
        anchor_id="",
        proof_present=True,
    )

