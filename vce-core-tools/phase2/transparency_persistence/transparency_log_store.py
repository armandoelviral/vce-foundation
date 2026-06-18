from phase2.transparency_persistence.transparency_entry_record import (
    TransparencyEntryRecord,
)


class TransparencyLogStore:

    def __init__(self):

        self._entries = {}

    def add(
        self,
        entry: TransparencyEntryRecord,
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

    def all(self):

        return list(
            self._entries.values()
        )
