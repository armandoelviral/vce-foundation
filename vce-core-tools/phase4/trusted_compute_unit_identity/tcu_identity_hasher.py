import hashlib
import json


class TcuIdentityHasher:

    @staticmethod
    def hash_identity(identity_block):

        canonical = json.dumps(
            identity_block.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
        )

        return hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()
