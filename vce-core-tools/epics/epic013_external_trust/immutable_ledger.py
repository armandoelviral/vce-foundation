import hashlib
import json


class ImmutableLedgerStore:

    def __init__(self):
        self.records = []
        self.previous_hash = "GENESIS"

    def append(self, entry):

        canonical = json.dumps(
            entry,
            sort_keys=True,
            separators=(",", ":")
        )

        current_hash = hashlib.sha256(
            (
                self.previous_hash +
                canonical
            ).encode()
        ).hexdigest()

        record = {
            "entry": entry,
            "previous_hash": self.previous_hash,
            "current_hash": current_hash,
        }

        self.records.append(record)
        self.previous_hash = current_hash

        return record

    def verify(self):

        expected_previous = "GENESIS"

        for record in self.records:

            if record["previous_hash"] != expected_previous:
                return False

            canonical = json.dumps(
                record["entry"],
                sort_keys=True,
                separators=(",", ":")
            )

            expected_current = hashlib.sha256(
                (
                    expected_previous +
                    canonical
                ).encode()
            ).hexdigest()

            if record["current_hash"] != expected_current:
                return False

            expected_previous = record["current_hash"]

        return True
