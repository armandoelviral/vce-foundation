import hashlib
import json
import time


class CryptographicAuditChain:

    def __init__(self):

        self.chain = []


    def append(
        self,
        event
    ):

        previous_hash = (
            self.chain[-1]["entry_hash"]
            if self.chain
            else "GENESIS"
        )

        entry = {
            "timestamp": int(
                time.time()
            ),
            "event": event,
            "previous_hash": previous_hash
        }

        canonical = json.dumps(
            entry,
            sort_keys=True,
            separators=(",", ":")
        )

        digest = hashlib.sha256(
            canonical.encode()
        ).hexdigest()

        record = {
            "entry": entry,
            "entry_hash": digest
        }

        self.chain.append(
            record
        )

        return record


    def verify(
        self
    ):

        previous = "GENESIS"

        for record in self.chain:

            entry = record[
                "entry"
            ]

            if (
                entry[
                    "previous_hash"
                ]
                != previous
            ):
                return False

            expected = hashlib.sha256(
                json.dumps(
                    entry,
                    sort_keys=True,
                    separators=(",", ":")
                ).encode()
            ).hexdigest()

            if (
                expected
                !=
                record[
                    "entry_hash"
                ]
            ):
                return False

            previous = record[
                "entry_hash"
            ]

        return True
