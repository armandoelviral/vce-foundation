from sp001.contracts.case_access_issuance_completion import (
    CaseAccessIssuanceCompletion,
)
from sp001.services.prepared_case_access_completion import (
    PreparedCaseAccessCompleter,
)

from sp001.contracts.protected_case_access_credential import (
    ProtectedCaseAccessCredential,
)
from sp001.infrastructure.sqlite_case_access_issuance_preparations import (
    SqliteCaseAccessIssuancePreparations, _serialize,
)




class SqliteCaseAccessIssuanceCompletions(SqliteCaseAccessIssuancePreparations):
    """Trusted storage capability; completion does not authenticate its caller."""

    def __init__(self, *, database_path):
        super().__init__(database_path=database_path)
        with self._connection() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS case_access_issuance_completions (
                    request_id TEXT PRIMARY KEY
                        REFERENCES case_access_issuance_preparations(request_id),
                    status TEXT NOT NULL CHECK(status='COMPLETED'),
                    completed_at INTEGER NOT NULL CHECK(completed_at>=0),
                    protection_key_id TEXT NOT NULL,
                    nonce BLOB NOT NULL CHECK(length(nonce)=12),
                    ciphertext BLOB NOT NULL CHECK(length(ciphertext)>16)
                );
            """)

    @staticmethod
    def _completion(row):
        return CaseAccessIssuanceCompletion(
            request_id=row[0], completed_at=row[1],
            protected=ProtectedCaseAccessCredential(row[2], row[3], row[4]),
        )

    def read_completed(self, *, request_id):
        """Historical evidence only; this read does not authorize token delivery."""
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("request_id must be a nonempty string")
        with self._connection() as connection:
            row = connection.execute(
                """SELECT request_id, completed_at, protection_key_id, nonce,
                ciphertext FROM case_access_issuance_completions WHERE request_id=?""",
                (request_id,),
            ).fetchone()
        return None if row is None else self._completion(row)

    def confirm(self, *, preparation, protected, clock, before_commit=None):
        if not isinstance(protected, ProtectedCaseAccessCredential):
            raise TypeError("protected must be a ProtectedCaseAccessCredential")
        if not callable(clock):
            raise TypeError("clock must be callable")
        document = _serialize(preparation)
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute(
                    """SELECT document FROM case_access_issuance_preparations
                    WHERE request_id=?""", (preparation.request_id,),
                ).fetchone()
                if row is None or row[0] != document:
                    raise ValueError("exact persisted preparation is required")

                # Obtain time after acquiring the write lock, including lock waits.
                at_time = clock()
                self._validate_references(
                    connection=connection, preparation=preparation, at_time=at_time,
                )
                existing = connection.execute(
                    """SELECT request_id, completed_at, protection_key_id, nonce,
                    ciphertext FROM case_access_issuance_completions
                    WHERE request_id=?""", (preparation.request_id,),
                ).fetchone()
                if existing is None:
                    connection.execute(
                        """INSERT INTO case_access_issuance_completions
                        (request_id, status, completed_at, protection_key_id,
                         nonce, ciphertext) VALUES (?, 'COMPLETED', ?, ?, ?, ?)""",
                        (preparation.request_id, at_time, protected.protection_key_id,
                         protected.nonce, protected.ciphertext),
                    )
                    existing = (
                        preparation.request_id, at_time, protected.protection_key_id,
                        protected.nonce, protected.ciphertext,
                    )
                result = self._completion(existing)
                if before_commit is not None:
                    before_commit()
                connection.commit()
                return result
            except BaseException:
                connection.rollback()
                raise
