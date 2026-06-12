import hashlib


class CertificateSignature:

    @staticmethod
    def sign(certificate_hash: str) -> str:
        return hashlib.sha256(
            certificate_hash.encode()
        ).hexdigest()
