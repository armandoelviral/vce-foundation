import hashlib
import json
import time


class SlashingEvidence:

    def create(
        self,
        violation
    ):

        evidence = {
            "violation": violation,
            "timestamp": int(
                time.time()
            )
        }


        canonical = json.dumps(
            evidence,
            sort_keys=True,
            separators=(",", ":")
        )


        digest = hashlib.sha256(
            canonical.encode()
        ).hexdigest()


        return {
            "evidence": evidence,
            "evidence_hash": digest,
            "slashable": True
        }


    def verify(
        self,
        record
    ):

        expected = hashlib.sha256(
            json.dumps(
                record["evidence"],
                sort_keys=True,
                separators=(",", ":")
            ).encode()
        ).hexdigest()


        return (
            expected
            ==
            record[
                "evidence_hash"
            ]
        )
