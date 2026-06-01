class ReleaseCandidateGate:

    REQUIRED_CHECKS = [
        "secure_execution",
        "hardening",
        "trust",
        "ledger",
        "audit",
        "recovery"
    ]


    def validate(self, report):

        for check in self.REQUIRED_CHECKS:

            if report.get(check) is not True:
                return {
                    "release": False,
                    "failed": check
                }


        return {
            "release": True,
            "version": "v0.1-rc"
        }
