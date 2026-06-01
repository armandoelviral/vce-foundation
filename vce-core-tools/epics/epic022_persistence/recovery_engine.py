import json
import sqlite3


class RecoveryEngine:

    def __init__(self, db_path):
        self.db_path = db_path

    def latest_entry(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT entry_type, payload
            FROM ledger
            ORDER BY id DESC
            LIMIT 1
            """
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return {
            "entry_type": row[0],
            "payload": json.loads(row[1])
        }

    def recover_checkpoint(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT payload
            FROM ledger
            WHERE entry_type = 'CHECKPOINT'
            ORDER BY id DESC
            LIMIT 1
            """
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return {
                "recovered": False,
                "reason": "NO_CHECKPOINT"
            }

        return {
            "recovered": True,
            "checkpoint": json.loads(row[0])
        }
