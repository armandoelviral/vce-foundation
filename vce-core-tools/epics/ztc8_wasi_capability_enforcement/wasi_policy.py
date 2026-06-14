class WASIPolicy:

    ALLOWED = {
        "stdout",
    }

    @classmethod
    def allow(
        cls,
        capability: str,
    ) -> bool:

        return capability in cls.ALLOWED
