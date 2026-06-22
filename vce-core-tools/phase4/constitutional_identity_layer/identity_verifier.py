class IdentityVerifier:

    @staticmethod
    def verify(identity) -> bool:

        return (
            identity.sovereign
            and not identity.revoked
            and identity.continuous
        )
