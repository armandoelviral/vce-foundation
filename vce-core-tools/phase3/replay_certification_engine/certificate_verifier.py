from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)


class CertificateVerifier:

    @staticmethod
    def verify(
        certificate: ReplayCertificateRecord,
    ) -> bool:

        if not certificate.certificate_id:
            return False

        if not certificate.replay_id:
            return False

        if not certificate.status:
            return False

        return True
