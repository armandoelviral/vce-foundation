class LedgerApply:

    def __init__(self):

        self.local_ledger = [
            {
                "sequence": 1,
                "event": "BOOTSTRAP"
            },
            {
                "sequence": 2,
                "event": "ATTESTATION"
            }
        ]

    def apply(
        self,
        remote_ledger
    ):

        self.local_ledger = remote_ledger

    def current(self):

        return self.local_ledger
