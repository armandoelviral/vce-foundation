import hashlib
import json

from epics.ztc19_governance_ledger.governance_ledger_entry import (
    GovernanceLedgerEntry,
)


class GovernanceHashChain:

    def __init__(self):

        self._records = []

    def append(
        self,
        entry: GovernanceLedgerEntry,
    ) -> dict:

        previous_hash = (
            self._records[-1]["current_hash"]
            if self._records
            else "GENESIS"
        )

        payload = {
            "entry": entry.to_dict(),
            "previous_hash": previous_hash,
        }

        current_hash = hashlib.sha256(
            json.dumps(
                payload,
                sort_keys=True,
            ).encode()
        ).hexdigest()

        record = {
            "entry": entry.to_dict(),
            "previous_hash": previous_hash,
            "current_hash": current_hash,
        }

        self._records.append(record)

        return record
