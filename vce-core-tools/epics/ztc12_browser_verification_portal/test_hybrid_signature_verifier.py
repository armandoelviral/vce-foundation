from epics.ztc12_browser_verification_portal.hybrid_signature_verifier import (
    HybridSignatureVerifier,
)


def test_accepts_both_signatures():

    assert HybridSignatureVerifier.verify(
        classical_valid=True,
        pqc_valid=True,
    )


def test_rejects_missing_classical_signature():

    assert not HybridSignatureVerifier.verify(
        classical_valid=False,
        pqc_valid=True,
    )


def test_rejects_missing_pqc_signature():

    assert not HybridSignatureVerifier.verify(
        classical_valid=True,
        pqc_valid=False,
    )


def test_rejects_both_invalid():

    assert not HybridSignatureVerifier.verify(
        classical_valid=False,
        pqc_valid=False,
    )
