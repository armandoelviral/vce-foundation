import hashlib
import json


class RekorClient:

    def create_entry(
        self,
        artifact
    ):

        canonical = json.dumps(
            artifact,
            sort_keys=True,
            separators=(",", ":")
        )

        digest = hashlib.sha256(
            canonical.encode()
        ).hexdigest()


        return {
            "uuid": digest[:16],
            "artifact_hash": digest,
            "integrated_time": 1,
            "log_index": 1,
            "inclusion_proof": True
        }


    def verify_entry(
        self,
        entry
    ):

        required = [
            "uuid",
            "artifact_hash",
            "log_index",
            "inclusion_proof"
        ]


        for field in required:

            if field not in entry:
                return False


        return (
            entry["inclusion_proof"]
            is True
        )
