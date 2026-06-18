from phase3.replay_certification_engine.replay_certificate_registry import (
    ReplayCertificateRegistry,
)


class CertificateQuery:

    def __init__(
        self,
        registry: ReplayCertificateRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        certificate_id: str,
    ):

        return self.registry.get(
            certificate_id
        )
