import hashlib
import json


class ReplayAttackDetector:

    def __init__(self):

        self.seen = set()


    def fingerprint(self, event):

        canonical = json.dumps(
            event,
            sort_keys=True,
            separators=(",", ":")
        )

        return hashlib.sha256(
            canonical.encode()
        ).hexdigest()


    def validate(self, event):

        digest = self.fingerprint(
            event
        )

        if digest in self.seen:
            return False

        self.seen.add(
            digest
        )

        return True


    def validate_stream(self, events):

        for event in events:

            if not self.validate(
                event
            ):
                return False

        return True
