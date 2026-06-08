import hashlib

from dataclasses import replace


def sign_envelope(
    envelope,
    signing_key_id="runtime-dev-key",
):

    payload = envelope.signing_payload()

    signature = hashlib.sha256(
        payload.encode()
    ).hexdigest()

    return replace(
        envelope,
        signature=signature,
        signing_key_id=signing_key_id,
        signature_algorithm="SHA256-DEMO",
    )
