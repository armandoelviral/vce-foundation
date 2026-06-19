from phase3.certificate_transparency.transparency_log import (
    TransparencyLog,
)


class InclusionVerifier:

    @staticmethod
    def verify(
        log: TransparencyLog,
        entry_id: str,
    ) -> bool:

        return (
            log.get(
                entry_id
            )
            is not None
        )
