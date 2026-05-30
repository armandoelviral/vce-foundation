import hashlib


class HashChain:

    def __init__(self):

        self.current_hash = "GENESIS"

    def append(
        self,
        record
    ):

        payload = (
            self.current_hash +
            str(record)
        )

        self.current_hash = (
            hashlib.sha256(
                payload.encode()
            ).hexdigest()
        )

        return self.current_hash
