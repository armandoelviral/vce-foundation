import json
import sqlite3


class CrashConsistencyChecker:

    def __init__(self, db_path):
        self.db_path = db_path


    def verify(self):

        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT payload
            FROM ledger
            """
        )

        rows = cursor.fetchall()

        conn.close()

        try:

            for row in rows:

                json.loads(
                    row[0]
                )

            return {
                "consistent": True
            }

        except Exception:

            return {
                "consistent": False
            }
