class TcuRegistryMembership:

    @staticmethod
    def is_member(
        registry,
        did: str,
    ) -> bool:

        for entry in registry.entries:

            if (
                entry.did == did
                and entry.status == "ACTIVE"
            ):
                return True

        return False
