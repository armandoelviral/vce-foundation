class TcuRegistryVerifier:

    @staticmethod
    def verify(
        registry,
        did: str,
    ) -> bool:

        for entry in registry.entries:

            if entry.did != did:
                continue

            if entry.status != "ACTIVE":
                return False

            if not entry.identity_hash:
                return False

            if not entry.attestation_root:
                return False

            return True

        return False
