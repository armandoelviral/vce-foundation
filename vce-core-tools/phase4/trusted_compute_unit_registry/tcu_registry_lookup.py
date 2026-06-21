class TcuRegistryLookup:

    @staticmethod
    def by_did(
        registry,
        did: str,
    ):

        for entry in registry.entries:

            if entry.did == did:

                return entry

        return None
