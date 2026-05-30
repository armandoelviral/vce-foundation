import hashlib


class ReplayState:

    def __init__(self):

        self.sequence_number = 0
        self.events = []
        self.state_hash = self._calculate_hash()

    def append_event(
        self,
        event: str
    ):

        self.sequence_number += 1

        self.events.append(
            event
        )

        self.state_hash = (
            self._calculate_hash()
        )

    def _calculate_hash(self):

        payload = "|".join(
            self.events
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()
