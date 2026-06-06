import hashlib
import json
from dataclasses import asdict


class StateHasher:

    def hash(self, state):

        payload = json.dumps(
            asdict(state),
            sort_keys=True,
            separators=(",", ":"),
        )

        return hashlib.sha256(
            payload.encode("utf-8")
        ).hexdigest()
