from epics.ztc12_browser_verification_portal.browser_signature_verifier import (
    BrowserSignatureVerifier,
)


def test_accepts_matching_signature():

    assert BrowserSignatureVerifier.verify(
        signature="valid-signature",
        public_key="pk-001",
    )


def test_rejects_invalid_signature():

    assert not BrowserSignatureVerifier.verify(
        signature="invalid-signature",
        public_key="pk-001",
    )
