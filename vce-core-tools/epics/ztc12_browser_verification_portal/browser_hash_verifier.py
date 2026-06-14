import hashlib


class BrowserHashVerifier:

    @staticmethod
    def compute(
        payload: str,
    ) -> str:

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()

    @staticmethod
    def verify(
        payload: str,
        expected_hash: str,
    ) -> bool:

        return (
            BrowserHashVerifier.compute(
                payload
            )
            == expected_hash
        )
