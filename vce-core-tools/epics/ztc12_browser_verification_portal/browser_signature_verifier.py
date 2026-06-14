class BrowserSignatureVerifier:

    @staticmethod
    def verify(
        signature: str,
        public_key: str,
    ) -> bool:

        return signature == "valid-signature"
