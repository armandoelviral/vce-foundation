import hashlib


class ClassicalSignatureLayer:

    @staticmethod
    def sign(
        evidence_hash: str,
        key: str,
    ) -> str:

        payload = f"classical:{evidence_hash}:{key}"

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()
