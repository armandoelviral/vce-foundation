class DeterministicRecovery:

    def recover(self, ledger):

        if not ledger.verify():
            return {
                "recovered": False,
                "reason": "LEDGER_CORRUPTION"
            }


        if not ledger.records:
            return {
                "recovered": True,
                "state": "GENESIS"
            }


        latest = ledger.records[-1]

        return {
            "recovered": True,
            "state_hash": latest[
                "current_hash"
            ],
            "sequence": len(
                ledger.records
            )
        }
