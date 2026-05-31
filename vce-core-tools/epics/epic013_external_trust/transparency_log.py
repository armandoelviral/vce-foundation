import hashlib
import json


class TransparencyLog:

    def create_entry(self, artifact):

        canonical = json.dumps(
            artifact,
            sort_keys=True
        )

        digest = hashlib.sha256(
            canonical.encode()
        ).hexdigest()

        return {
            "log_index": 1,
            "artifact_hash": digest,
            "included": True
        }


    def verify_inclusion(self, entry):

        if not entry.get("included"):
            return False

        if "artifact_hash" not in entry:
            return False

        return True
