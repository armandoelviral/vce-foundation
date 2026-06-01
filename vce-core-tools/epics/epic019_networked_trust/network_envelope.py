import hashlib
import json


class NetworkEnvelope:

    def seal(
        self,
        message,
        sender_id
    ):

        payload = {
            "sender_id": sender_id,
            "message": message
        }


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
            envelope[
                "signature"
            ]
        )
