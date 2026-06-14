class HostImportPolicy:

    ALLOWED = {
        "memory",
        "arithmetic",
    }

    @classmethod
    def is_allowed(
        cls,
        capability: str,
    ) -> bool:

        return capability in cls.ALLOWED
