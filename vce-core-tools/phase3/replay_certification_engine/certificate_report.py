from phase3.replay_certification_engine.replay_certificate_registry import (
    ReplayCertificateRegistry,
)


class CertificateReport:

    def __init__(
        self,
        registry: ReplayCertificateRegistry,
    ):

        self.registry = registry

    def certificate_count(
        self,
    ) -> int:

        return self.registry.count()

    def certificate_ids(
        self,
    ):

        return [
            certificate.certificate_id
            for certificate in self.registry.certificates()
        ]

    def to_dict(
        self,
    ):

        return {
            "certificate_count":
                self.certificate_count(),
            "certificate_ids":
                self.certificate_ids(),
        }
