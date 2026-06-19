from phase3.certificate_transparency.transparency_certificate_record import (
    TransparencyCertificateRecord,
)


class TransparencyLog:

    def __init__(self):

        self._entries = {}

    def add(
        self,
        entry: TransparencyCertificateRecord,
    ) -> None:

        self._entries[
            entry.entry_id
        ] = entry

    def get(
        self,
        entry_id: str,
    ):

        return self._entries.get(
            entry_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._entries
        )

    def entries(
        self,
    ):

        return list(
            self._entries.values()
        )
