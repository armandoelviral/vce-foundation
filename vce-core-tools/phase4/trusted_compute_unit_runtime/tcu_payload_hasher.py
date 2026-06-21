import hashlib
import json


class TcuPayloadHasher:

    @staticmethod
    def hash_payload(payload):

        canonical = json.dumps(
            payload.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
        )

        return hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()
