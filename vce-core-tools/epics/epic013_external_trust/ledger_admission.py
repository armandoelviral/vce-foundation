import time


class LedgerAdmissionController:

    def admit(self, trust_result):

        if trust_result.get(
            "ledger_admission"
        ) != "APPROVED":

            return {
                "status": "REJECTED",
                "reason": "TRUST_FAILURE"
            }


        return {
            "status": "COMMITTED",
            "timestamp": int(
                time.time()
            ),
            "state_hash": trust_result[
                "state_hash"
            ],
            "sequence_number": trust_result[
                "sequence_number"
            ]
        }
