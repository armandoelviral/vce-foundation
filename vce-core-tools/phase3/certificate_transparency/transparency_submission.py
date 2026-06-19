from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.certificate_transparency.transparency_certificate_record import (
    TransparencyCertificateRecord,
)

from phase3.certificate_transparency.transparency_log import (
    TransparencyLog,
)


class TransparencySubmission:

    @staticmethod
    def submit(
        entry_id: str,
        certificate: ReplayCertificateRecord,
        log: TransparencyLog,
    ) -> TransparencyCertificateRecord:

        entry = (
            TransparencyCertificateRecord(
                entry_id=entry_id,
                certificate_id=(
                    certificate.certificate_id
                ),
            )
        )

        log.add(
            entry
        )

        return entry
