from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.replay_revocation.replay_revocation_record import (
    ReplayRevocationRecord,
)

from phase3.replay_revocation.revocation_registry import (
    RevocationRegistry,
)


class RevocationSubmission:

    @staticmethod
    def submit(
        revocation_id: str,
        certificate: ReplayCertificateRecord,
        reason: str,
        registry: RevocationRegistry,
    ) -> ReplayRevocationRecord:

        revocation = (
            ReplayRevocationRecord(
                revocation_id=revocation_id,
                certificate_id=(
                    certificate.certificate_id
                ),
                reason=reason,
            )
        )

        registry.add(
            revocation
        )

        return revocation
