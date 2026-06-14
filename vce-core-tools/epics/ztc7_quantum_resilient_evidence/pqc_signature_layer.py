import hashlib


class PQCSignatureLayer:

    @staticmethod
    def sign(
        evidence_hash: str,
        key: str,
    ) -> str:

        payload = f"pqc:{evidence_hash}:{key}"

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()
