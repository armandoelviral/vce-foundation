import json
import sqlite3


class NodeLedger:

    def __init__(self, db_path):
        self.db_path = db_path
        self.initialize()
       
    def initialize(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ledger (
                sequence INTEGER PRIMARY KEY,
                event TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )

        conn.commit()
        conn.close()

    def exists(self, sequence):
        return any(
            event["sequence"] == sequence
            for event in self.all()
        )
    
    def append(self, event):

        if self.exists(
            event["sequence"]
        ):
            return False

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO ledger (
                sequence,
                event,
                payload
            )
            VALUES (?, ?, ?)
            """,
            (
                event["sequence"],
                event["event"],
                json.dumps(event),
            )
        )

        conn.commit()
        conn.close()

        return True

    def all(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT payload
            FROM ledger
            ORDER BY sequence ASC
            """
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            json.loads(row[0])
            for row in rows
        ]

    def count(self):
        return len(self.all())

    def replace_all(
        self,
        events
    ):

        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM ledger
            """
        )

        for event in events:

            cursor.execute(
                """
                INSERT INTO ledger (
                    sequence,
                    event,
                    payload
                )
                VALUES (?, ?, ?)
                """,
                (
                    event["sequence"],
                    event.get(
                        "event",
                        "RECOVERED"
                    ),
                    json.dumps(event)
                )
            )

        conn.commit()
        conn.close()

        return len(events)
