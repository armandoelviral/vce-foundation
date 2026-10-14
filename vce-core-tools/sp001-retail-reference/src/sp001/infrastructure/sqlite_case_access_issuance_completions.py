from collections.abc import Callable
from dataclasses import dataclass
import time

from sp001.contracts.case_access_token_issuance import IssuedCaseAccessToken
from sp001.infrastructure.prepared_case_access_credentials import (
    PreparedCaseAccessSigner, PreparedCredentialProtector,
    ProtectedCaseAccessCredential,
)
from sp001.infrastructure.sqlite_case_access_issuance_preparations import (
    SqliteCaseAccessIssuancePreparations, _serialize,
)


@dataclass(frozen=True, slots=True)
class CaseAccessIssuanceCompletion:
    request_id: str
    completed_at: int
    protected: ProtectedCaseAccessCredential


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


class PreparedCaseAccessCompleter:
    """Internal issuance capability: sign, protect, confirm, then release."""

    def __init__(
        self, *, store: SqliteCaseAccessIssuanceCompletions,
        signer: PreparedCaseAccessSigner,
        protector: PreparedCredentialProtector,
        clock: Callable[[], int] | None = None,
    ):
        if not isinstance(store, SqliteCaseAccessIssuanceCompletions):
            raise TypeError("store must support durable completion")
        if not isinstance(signer, PreparedCaseAccessSigner):
            raise TypeError("signer must be a PreparedCaseAccessSigner")
        if not isinstance(protector, PreparedCredentialProtector):
            raise TypeError("protector must be a PreparedCredentialProtector")
        if clock is not None and not callable(clock):
            raise TypeError("clock must be callable")
        self._store = store
        self._signer = signer
        self._protector = protector
        self._clock = clock if clock is not None else lambda: int(time.time())

    def complete(self, *, request_id: str, before_commit=None) -> IssuedCaseAccessToken:
        preparation = self._store.read_prepared(request_id=request_id)
        if preparation is None:
            raise ValueError("persisted preparation is required")
        historical = self._store.read_completed(request_id=request_id)
        if historical is None:
            token = self._signer.sign(preparation=preparation)
            protected = self._protector.protect(
                preparation=preparation, token=token,
            )
        else:
            protected = historical.protected

        # Replays also revalidate current references. First completion wins.
        persisted = self._store.confirm(
            preparation=preparation, protected=protected, clock=self._clock,
            before_commit=before_commit,
        )
        return self._protector.recover(
            preparation=preparation, protected=persisted.protected,
        )
