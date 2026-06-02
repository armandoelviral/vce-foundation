class RecoveryApply:

    def __init__(self):

        self.local_state = {
            "node_id": "node-c",
            "sequence_number": 15,
            "state_hash": "old999",
            "ledger": []
        }

    def apply(
        self,
        remote_state
    ):

        self.local_state = remote_state

    def current(self):

        return self.local_state
