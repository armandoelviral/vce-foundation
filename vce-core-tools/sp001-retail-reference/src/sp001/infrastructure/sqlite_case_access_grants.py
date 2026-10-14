from sp001.contracts.case_access_grant_snapshot import CaseAccessGrantSnapshot
from contextlib import contextmanager
from dataclasses import asdict
import json
from pathlib import Path
import sqlite3

from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_context import (
    CaseAccessOperation, CaseAccessPermission,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)


def _document(value) -> str:
    return json.dumps(
        asdict(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )


def _grant(value) -> CaseAccessGrant:
    return CaseAccessGrant(
        grant_id=value["grant_id"],
        principal=AuthenticatedPrincipal(**value["principal"]),
        permission=CaseAccessPermission(
            case_id=value["permission"]["case_id"],
            operation=CaseAccessOperation(value["permission"]["operation"]),
        ),
        valid_from=value["valid_from"], expires_at=value["expires_at"],
    )


class SqliteCaseAccessGrants:
    """Trusted storage capability; administration service supplies authorization."""

    def __init__(self, *, database_path: str | Path) -> None:
        if not isinstance(database_path, (str, Path)):
            raise TypeError("database_path must be a string or Path")
        if not str(database_path).strip() or str(database_path) == ":memory:":
            raise ValueError("database_path must identify a persistent file")
        self._path = str(database_path)
        with self._connection() as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS case_access_grants (
                    grant_id TEXT PRIMARY KEY,
                    definition TEXT NOT NULL,
                    issuer TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    case_id TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    valid_from INTEGER NOT NULL,
                    expires_at INTEGER NOT NULL,
                    revoked INTEGER NOT NULL DEFAULT 0 CHECK(revoked IN (0, 1))
                );
                CREATE INDEX IF NOT EXISTS case_access_grants_lookup
                ON case_access_grants(issuer, subject, case_id, operation);
                CREATE TABLE IF NOT EXISTS case_access_grant_audit (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE,
                    grant_id TEXT NOT NULL REFERENCES case_access_grants(grant_id),
                    record TEXT NOT NULL
                );
            """)

    @contextmanager
    def _connection(self):
        connection = sqlite3.connect(self._path)
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("PRAGMA synchronous=FULL")
            yield connection
        finally:
            connection.close()

    def apply(self, *, record: GrantAdministrationRecord) -> bool:
        if not isinstance(record, GrantAdministrationRecord):
            raise TypeError("record must be a GrantAdministrationRecord")
        serialized = _document(record)
        grant = record.grant
        definition = _document(grant)
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                existing_event = connection.execute(
                    "SELECT record FROM case_access_grant_audit WHERE event_id=?",
                    (record.event_id,),
                ).fetchone()
                if existing_event is not None:
                    if existing_event[0] != serialized:
                        raise ValueError("event_id conflicts with stored record")
                    connection.commit()
                    return True

                existing = connection.execute(
                    "SELECT definition, revoked FROM case_access_grants WHERE grant_id=?",
                    (grant.grant_id,),
                ).fetchone()
                if existing is not None and existing[0] != definition:
                    raise ValueError("grant_id conflicts with stored definition")

                if record.action is Action.GRANT:
                    if existing is not None and existing[1]:
                        raise ValueError("revoked grant_id cannot be reactivated")
                    if existing is None:
                        connection.execute(
                            """INSERT INTO case_access_grants
                            (grant_id, definition, issuer, subject, case_id,
                             operation, valid_from, expires_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                            (
                                grant.grant_id, definition,
                                grant.principal.issuer, grant.principal.subject,
                                grant.permission.case_id, grant.permission.operation.value,
                                grant.valid_from, grant.expires_at,
                            ),
                        )
                else:
                    if existing is None:
                        connection.rollback()
                        return False
                    connection.execute(
                        "UPDATE case_access_grants SET revoked=1 WHERE grant_id=?",
                        (grant.grant_id,),
                    )

                connection.execute(
                    """INSERT INTO case_access_grant_audit
                    (event_id, grant_id, record) VALUES (?, ?, ?)""",
                    (record.event_id, grant.grant_id, serialized),
                )
                connection.commit()
                return True
            except BaseException:
                connection.rollback()
                raise

    def permits(
        self, *, principal: AuthenticatedPrincipal,
        permission: CaseAccessPermission, at_time: int,
    ) -> bool:
        if not isinstance(principal, AuthenticatedPrincipal):
            raise TypeError("principal must be an AuthenticatedPrincipal")
        if not isinstance(permission, CaseAccessPermission):
            raise TypeError("permission must be a CaseAccessPermission")
        if isinstance(at_time, bool) or not isinstance(at_time, int):
            raise TypeError("at_time must be integer Unix seconds")
        if at_time < 0:
            raise ValueError("at_time must not be negative")
        with self._connection() as connection:
            result = connection.execute(
                """SELECT 1 FROM case_access_grants
                WHERE issuer=? AND subject=? AND case_id=? AND operation=?
                AND revoked=0 AND valid_from<=? AND expires_at>?
                LIMIT 1""",
                (
                    principal.issuer, principal.subject,
                    permission.case_id, permission.operation.value,
                    at_time, at_time,
                ),
            ).fetchone()
            return result is not None

    def read_grant_snapshot(
        self, *, grant_id: str
    ) -> CaseAccessGrantSnapshot | None:
        if not isinstance(grant_id, str):
            raise TypeError("grant_id must be a string")
        if not grant_id.strip():
            raise ValueError("grant_id must not be empty")
        with self._connection() as connection:
            row = connection.execute(
                """SELECT g.definition, g.revoked,
                (SELECT COUNT(*) FROM case_access_grant_audit AS a
                 WHERE a.grant_id=g.grant_id)
                FROM case_access_grants AS g WHERE g.grant_id=?""",
                (grant_id,),
            ).fetchone()
        if row is None:
            return None
        if row[1] not in (0, 1) or row[2] < 1:
            raise ValueError("inconsistent persistent grant snapshot")
        grant = _grant(json.loads(row[0]))
        if grant.grant_id != grant_id:
            raise ValueError("stored grant identity mismatch")
        return CaseAccessGrantSnapshot(
            grant=grant, revision=row[2], revoked=bool(row[1]),
        )

    def read_audit(self) -> tuple[GrantAdministrationRecord, ...]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT record FROM case_access_grant_audit ORDER BY sequence"
            ).fetchall()
        records = []
        for row in rows:
            value = json.loads(row[0])
            records.append(GrantAdministrationRecord(
                event_id=value["event_id"],
                actor=AuthenticatedPrincipal(**value["actor"]),
                action=Action(value["action"]),
                grant=_grant(value["grant"]),
                recorded_at=value["recorded_at"],
            ))
        return tuple(records)
