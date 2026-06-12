from epics.epic088_replay_provenance_certificate.certificate_signature import (
    CertificateSignature,
)


class CertificateVerifier:

    @staticmethod
    def verify(
        certificate_hash: str,
        signature: str,
    ) -> bool:

        expected_signature = (
            CertificateSignature.sign(
                certificate_hash
            )
        )

        return signature == expected_signature
