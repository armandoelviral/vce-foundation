import hashlib
import json


class SignedRequest:

    def sign(
        self,
        payload
    ):

        canonical = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        )

        signature = hashlib.sha256(
            canonical.encode()
        ).hexdigest()

        return {
            "payload": payload,
            "signature": signature
        }


    def verify(
        self,
        envelope
    ):

        canonical = json.dumps(
            envelope["payload"],
            sort_keys=True,
            separators=(",", ":")
        )

        expected = hashlib.sha256(
            canonical.encode()
        ).hexdigest()

        return (
            expected
            ==
            envelope["signature"]
        )
