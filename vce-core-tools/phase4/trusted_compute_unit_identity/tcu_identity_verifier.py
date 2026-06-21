class TcuIdentityVerifier:

    @staticmethod
    def verify(record):

        if not record.identity.did:
            return False

        if not record.identity_hash:
            return False

        if not record.identity.ed25519_public_key:
            return False

        if not record.identity.mldsa65_public_key:
            return False

        if not (
            record.signatures.ed25519_signature
        ):
            return False

        if not (
            record.signatures.mldsa65_signature
        ):
            return False

        return True
