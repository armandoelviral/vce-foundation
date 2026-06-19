from phase3.replay_revocation.revocation_registry import (
    RevocationRegistry,
)


class RevocationVerifier:

    @staticmethod
    def is_revoked(
        registry: RevocationRegistry,
        certificate_id: str,
    ) -> bool:

        for revocation in registry.revocations():

            if (
                revocation.certificate_id
                == certificate_id
            ):
                return True

        return False
