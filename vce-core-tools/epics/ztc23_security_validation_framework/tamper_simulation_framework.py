class TamperSimulationFramework:

    def tamper(
        self,
        record: dict,
        field: str,
        value,
    ) -> dict:

        tampered = dict(
            record
        )

        tampered[field] = value

        return tampered
