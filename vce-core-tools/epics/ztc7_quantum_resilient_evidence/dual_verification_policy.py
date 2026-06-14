class DualVerificationPolicy:

    @staticmethod
    def verify(
        classical_valid: bool,
        pqc_valid: bool,
        mode: str,
    ) -> bool:

        if mode == "strict_now":
            return (
                classical_valid
                and
                pqc_valid
            )

        if mode == "future_resilience":
            return (
                classical_valid
                or
                pqc_valid
            )

        if mode == "migration_mode":
            return (
                classical_valid
                or
                pqc_valid
            )

        return False
