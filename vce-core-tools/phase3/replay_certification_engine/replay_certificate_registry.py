from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)


class ReplayCertificateRegistry:

    def __init__(self):

        self._certificates = {}

    def add(
        self,
        certificate: ReplayCertificateRecord,
    ) -> None:

        self._certificates[
            certificate.certificate_id
        ] = certificate

    def get(
        self,
        certificate_id: str,
    ):

        return self._certificates.get(
            certificate_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._certificates
        )

    def certificates(
        self,
    ):

        return list(
            self._certificates.values()
        )
