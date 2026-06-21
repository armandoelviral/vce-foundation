class TcuRegistryRevocation:

    @staticmethod
    def revoke(
        registry,
        did: str,
    ) -> bool:

        for entry in registry.entries:

            if entry.did == did:

                entry.status = "REVOKED"

                return True

        return False
