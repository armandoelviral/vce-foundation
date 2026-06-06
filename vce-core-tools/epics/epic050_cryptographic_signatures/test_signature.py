from epics.epic050_cryptographic_signatures.signer import Signer


def test_signer_produces_deterministic_signature():

    signer = Signer(
        secret="test-secret",
    )

    payload = "abc123"

    signature_a = signer.sign(payload)
    signature_b = signer.sign(payload)

    assert signature_a == signature_b


def test_verifies_valid_signature():

    signer = Signer(
        secret="test-secret",
    )

    payload = "abc123"

    signature = signer.sign(payload)

    assert signer.verify(
        payload,
        signature,
    ) is True


def test_rejects_invalid_signature():

    signer = Signer(
        secret="test-secret",
    )

    payload = "abc123"

    assert signer.verify(
        payload,
        "bad-signature",
    ) is False
