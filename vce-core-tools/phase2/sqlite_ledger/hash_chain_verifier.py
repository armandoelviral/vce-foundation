from pathlib import Path

from phase2.sqlite_ledger.event_query import (
    EventQuery,
)


class HashChainVerifier:

    def __init__(
        self,
        db_path: Path,
    ):

        self.db_path = Path(
            db_path
        )

    def verify(
        self,
    ) -> bool:

        rows = EventQuery(
            self.db_path
        ).all()

        expected_previous = (
            "GENESIS"
        )

        for row in rows:

            if (
                row["previous_hash"]
                != expected_previous
            ):
                return False

            expected_previous = (
                row["current_hash"]
            )

        return True
