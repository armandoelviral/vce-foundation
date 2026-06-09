import hashlib


def verify_signature(
    envelope,
):

    if envelope.signature is None:
        return False

    expected_signature = hashlib.sha256(
        envelope.signing_payload().encode()
    ).hexdigest()

    return envelope.signature == expected_signature
