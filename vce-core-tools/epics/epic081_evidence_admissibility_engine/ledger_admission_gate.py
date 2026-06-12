class LedgerAdmissionGate:

    def can_write(
        self,
        admission_decision,
    ):

        return admission_decision.admitted is True

    def write_decision(
        self,
        admission_decision,
    ):

        if self.can_write(
            admission_decision
        ):
            return {
                "ledger_write_allowed": True,
                "admission_status": "ADMITTED",
            }

        return {
            "ledger_write_allowed": False,
            "admission_status": "REJECTED",
            "rejection_reason": admission_decision.reason,
        }
