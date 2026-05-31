import hashlib


class PersistentWAL:

    def __init__(self):

        self.previous_hash = "GENESIS"


    def append(self, lsn, opcode, payload):

        raw = (
            str(lsn)
            + opcode
            + payload
            + self.previous_hash
        )

        current_hash = hashlib.sha256(
            raw.encode()
        ).hexdigest()

        record = {
            "lsn": lsn,
            "opcode": opcode,
            "payload": payload,
            "previous_hash": self.previous_hash,
            "current_hash": current_hash,
        }

        self.previous_hash = current_hash

        return record
