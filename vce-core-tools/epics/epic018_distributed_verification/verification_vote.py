import hashlib
import json


class VerificationVote:

    def create(
        self,
        node,
        artifact_hash,
        decision
    ):

        payload = {
            "node_id": node[
                "node_id"
            ],
            "artifact_hash": artifact_hash,
            "decision": decision
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
        vote
    ):

        canonical = json.dumps(
            vote["payload"],
            sort_keys=True,
            separators=(",", ":")
        )


        expected = hashlib.sha256(
            canonical.encode()
        ).hexdigest()


        return (
            expected
            ==
            vote["signature"]
        )
