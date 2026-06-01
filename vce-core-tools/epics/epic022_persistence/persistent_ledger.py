import sqlite3
import json


class PersistentLedger:

    def __init__(self, db_path="ledger.db"):
        self.db_path = db_path
        self.initialize()

    def initialize(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_type TEXT NOT NULL,
                payload TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def append(self, entry_type, payload):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO ledger
            (
                entry_type,
                payload
            )
            VALUES (?, ?)
            """,
            (
                entry_type,
                json.dumps(payload)
            )
        )

        conn.commit()
        conn.close()

        return True

    def count(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM ledger"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count           
