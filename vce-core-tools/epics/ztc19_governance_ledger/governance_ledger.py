from typing import List

from epics.ztc19_governance_ledger.governance_ledger_entry import (
    GovernanceLedgerEntry,
)


class GovernanceLedger:

    def __init__(self):

        self._entries: List[
            GovernanceLedgerEntry
        ] = []

    def append(
        self,
        entry: GovernanceLedgerEntry,
    ) -> None:

        self._entries.append(
            entry
        )

    def all(
        self,
    ) -> List[GovernanceLedgerEntry]:

        return list(
            self._entries
        )

    def count(
        self,
    ) -> int:

        return len(
            self._entries
        )
