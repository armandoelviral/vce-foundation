"""Transactional authorization register for deployment inside the MVP1 authority."""

from contextlib import closing, contextmanager
from dataclasses import dataclass
from pathlib import Path
import sqlite3
from time import time

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from sp001.contracts.product001_mvp1_authorization_eligibility import (
    authorization_digest,
)
from sp001.contracts.product001_mvp1_contextual_authorization import (
    ContextualAuthorizationV1,
    decision_digest_from_canonical_bytes,
    verify_contextual_authorization_signature,
)


class AuthorizationConflict(ValueError):
    """The operation identity is already bound to a different authorization."""


@dataclass(frozen=True, slots=True)
class DurableAuthorizationIntent:
    issuer_id: str
    organization_id: str
    operation_id: str
    authorization_digest: str
    materialize_deadline: int
    decision_bytes: bytes


@dataclass(frozen=True, slots=True)
class AuthorizationTransition:
    sequence: int
    kind: str


@dataclass(frozen=True, slots=True)
class AuthorizationHistory:
    authorization_digest: str
    transitions: tuple[AuthorizationTransition, ...]
    complete: bool


class SqliteMvp1AuthorizationStore:
    """Internal authority API backed by a dedicated database.

    The authority owns the path, clock, key and registration/revocation calls.
    Context arguments must come from the authority's verified decision context.
    A durable intent is evidence inside this register, with no destination API.
    """

    def __init__(
        self,
        *,
        database_path: Path,
        issuer_id: str,
        public_key: Ed25519PublicKey,
        clock=lambda: int(time()),
        read_only: bool = False,
    ):
        if not issuer_id or type(issuer_id) is not str:
            raise ValueError("issuer identity required")
        if not isinstance(public_key, Ed25519PublicKey) or not callable(clock):
            raise TypeError("authority verification key and clock required")
        self._path = Path(database_path).resolve()
        self._issuer_id = issuer_id
        self._public_key = public_key
        self._clock = clock
        if type(read_only) is not bool:
            raise TypeError("read_only must be a boolean")
        self._read_only = read_only
        if read_only:
            return
        with closing(self._connect()) as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS mvp1_authorizations (
                    issuer_id TEXT NOT NULL,
                    organization_id TEXT NOT NULL,
                    operation_id TEXT NOT NULL,
                    digest TEXT NOT NULL,
                    authority_sequence TEXT NOT NULL,
                    revoked INTEGER NOT NULL DEFAULT 0 CHECK (revoked IN (0, 1)),
                    PRIMARY KEY (issuer_id, organization_id, operation_id)
                );
                CREATE TABLE IF NOT EXISTS mvp1_authorization_intents (
                    issuer_id TEXT NOT NULL,
                    organization_id TEXT NOT NULL,
                    operation_id TEXT NOT NULL,
                    deadline TEXT NOT NULL,
                    decision_bytes BLOB NOT NULL,
                    PRIMARY KEY (issuer_id, organization_id, operation_id),
                    FOREIGN KEY (issuer_id, organization_id, operation_id)
                        REFERENCES mvp1_authorizations
                );
                CREATE TABLE IF NOT EXISTS mvp1_authorization_transitions (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    issuer_id TEXT NOT NULL,
                    organization_id TEXT NOT NULL,
                    operation_id TEXT NOT NULL,
                    kind TEXT NOT NULL CHECK (kind IN ('CONSUMED', 'REVOKED')),
                    UNIQUE (issuer_id, organization_id, operation_id, kind),
                    FOREIGN KEY (issuer_id, organization_id, operation_id)
                        REFERENCES mvp1_authorizations
                );
            """)

    def _connect(self, *, read_only=False):
        if self._read_only and not read_only:
            raise PermissionError("authority register opened for recovery only")
        target = self._path.as_uri() + ("?mode=ro" if read_only else "")
        connection = sqlite3.connect(target, isolation_level=None, uri=True)
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("PRAGMA synchronous=FULL")
        except BaseException:
            connection.close()
            raise
        return connection

    @contextmanager
    def _write(self):
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            with connection:
                yield connection

    def _verify(self, cert, *, operation_id, decision_bytes, documentary_key):
        verify_contextual_authorization_signature(
            cert,
            trusted_issuer_id=self._issuer_id,
            trusted_public_key=self._public_key,
            expected_operation_id=operation_id,
            expected_decision_digest=decision_digest_from_canonical_bytes(decision_bytes),
            expected_documentary_key=documentary_key,
        )
        return (self._issuer_id, documentary_key.organization_id, operation_id)

    @staticmethod
    def _state(connection, identity, digest):
        row = connection.execute(
            "SELECT digest, authority_sequence, revoked FROM mvp1_authorizations "
            "WHERE issuer_id=? AND organization_id=? AND operation_id=?",
            identity,
        ).fetchone()
        if row is not None and row[0] != digest:
            raise AuthorizationConflict("operation authorization digest conflict")
        return row

    def register(
        self, cert: ContextualAuthorizationV1, *, operation_id, decision_bytes,
        documentary_key,
    ) -> bool:
        """Bind a verified authorization once, without reopening an operation."""
        identity = self._verify(
            cert, operation_id=operation_id, decision_bytes=decision_bytes,
            documentary_key=documentary_key,
        )
        digest = authorization_digest(cert)
        with self._write() as connection:
            if self._state(connection, identity, digest) is not None:
                return False
            connection.execute(
                "INSERT INTO mvp1_authorizations "
                "(issuer_id, organization_id, operation_id, digest, authority_sequence) "
                "VALUES (?, ?, ?, ?, ?)",
                (*identity, digest, str(cert.authority_sequence)),
            )
        return True

    def revoke(self, *, organization_id, operation_id, expected_digest) -> bool:
        identity = (self._issuer_id, organization_id, operation_id)
        with self._write() as connection:
            state = self._state(connection, identity, expected_digest)
            if state is None:
                raise PermissionError("authorization is unregistered")
            if state[2]:
                return False
            connection.execute(
                "UPDATE mvp1_authorizations SET revoked=1 "
                "WHERE issuer_id=? AND organization_id=? AND operation_id=?",
                identity,
            )
            self._append_transition(connection, identity, "REVOKED")
        return True

    def consume(
        self, cert: ContextualAuthorizationV1, *, operation_id, decision_bytes,
        documentary_key,
    ) -> DurableAuthorizationIntent:
        identity = self._verify(
            cert, operation_id=operation_id, decision_bytes=decision_bytes,
            documentary_key=documentary_key,
        )
        digest = authorization_digest(cert)
        intent = DurableAuthorizationIntent(
            *identity, digest, cert.materialize_deadline, decision_bytes,
        )
        with self._write() as connection:
            state = self._state(connection, identity, digest)
            if state is None or state[1] != str(cert.authority_sequence) or state[2]:
                raise PermissionError("authorization is absent, superseded or revoked")
            if self._read_intent(connection, identity) is not None:
                raise PermissionError("authorization already consumed")

            now = self._clock()
            if type(now) is not int or now < 0:
                raise ValueError("invalid authority clock")
            if now >= cert.materialize_deadline:
                raise PermissionError("materialization deadline expired")

            # The unique intent row is also the durable consumption marker.
            connection.execute(
                "INSERT INTO mvp1_authorization_intents VALUES (?, ?, ?, ?, ?)",
                (*identity, str(cert.materialize_deadline), decision_bytes),
            )
            self._append_transition(connection, identity, "CONSUMED")
        return intent

    @staticmethod
    def _append_transition(connection, identity, kind):
        connection.execute(
            "INSERT INTO mvp1_authorization_transitions "
            "(issuer_id, organization_id, operation_id, kind) VALUES (?, ?, ?, ?)",
            (*identity, kind),
        )

    def read_history(
        self, *, organization_id, operation_id, expected_digest,
    ) -> AuthorizationHistory | None:
        """Read observed transitions in local sequence order, with coverage."""
        identity = (self._issuer_id, organization_id, operation_id)
        with closing(self._connect(read_only=True)) as connection:
            connection.execute("BEGIN")
            state = self._state(connection, identity, expected_digest)
            if state is None:
                return None
            has_history_table = connection.execute(
                "SELECT 1 FROM sqlite_master "
                "WHERE type='table' AND name='mvp1_authorization_transitions'",
            ).fetchone()
            rows = ()
            if has_history_table:
                rows = connection.execute(
                    "SELECT sequence, kind FROM mvp1_authorization_transitions "
                    "WHERE issuer_id=? AND organization_id=? AND operation_id=? "
                    "ORDER BY sequence",
                    identity,
                ).fetchall()
            kinds = {kind for _, kind in rows}
            expected_kinds = set()
            if state[2]:
                expected_kinds.add("REVOKED")
            if self._read_intent(connection, identity) is not None:
                expected_kinds.add("CONSUMED")
            return AuthorizationHistory(
                authorization_digest=state[0],
                transitions=tuple(AuthorizationTransition(*row) for row in rows),
                complete=kinds == expected_kinds,
            )

    @staticmethod
    def _read_intent(connection, identity):
        return connection.execute(
            "SELECT deadline, decision_bytes FROM mvp1_authorization_intents "
            "WHERE issuer_id=? AND organization_id=? AND operation_id=?",
            identity,
        ).fetchone()

    def recover(self, *, organization_id, operation_id, expected_digest):
        """Read the original intent. Read errors propagate as unknown outcomes."""
        identity = (self._issuer_id, organization_id, operation_id)
        with closing(self._connect(read_only=True)) as connection:
            connection.execute("BEGIN")
            state = self._state(connection, identity, expected_digest)
            if state is None:
                return None
            row = self._read_intent(connection, identity)
            if row is None:
                return None
            return DurableAuthorizationIntent(*identity, state[0], int(row[0]), row[1])
