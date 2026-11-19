"""Internal SQLite commercial grant storage; no administrative authority."""

from dataclasses import asdict
from pathlib import Path
import json
import sqlite3

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)
from sp001.contracts.product001_commercial_approval_grant import (
    Product001CommercialApprovalGrant,
    Product001CommercialApprovalOperation,
)


class CommercialApprovalStorageConflict(ValueError):
    pass


def _json(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


def _selection(value):
    return KnowledgeScopeSelection(
        mode=KnowledgeScopeMode(value["mode"]),
        ids=tuple(value["ids"]),
    )


def _restore_grant(document):
    value = json.loads(document)
    scope = value["scope"]
    return Product001CommercialApprovalGrant(
        grant_id=value["grant_id"],
        principal=AuthenticatedPrincipal(**value["principal"]),
        operation=Product001CommercialApprovalOperation(
            value["operation"]
        ),
        scope=KnowledgeSourceScope(
            organization_id=scope["organization_id"],
            customer_id=scope["customer_id"],
            jurisdiction=scope["jurisdiction"],
            commercial_channel_id=scope["commercial_channel_id"],
            document_type=KnowledgeDocumentType(
                scope["document_type"]
            ),
            point_of_sale_scope=_selection(
                scope["point_of_sale_scope"]
            ),
            department_scope=_selection(
                scope["department_scope"]
            ),
            campaign_id=scope["campaign_id"],
        ),
        valid_from=value["valid_from"],
        expires_at=value["expires_at"],
    )


class SqliteProduct001CommercialApproval:
    """Privileged internal capability, not an authenticated API."""

    def __init__(self, *, database_path: str | Path):
        if not isinstance(database_path, (str, Path)):
            raise TypeError("invalid database path")
        if (
            not str(database_path).strip()
            or str(database_path) == ":memory:"
        ):
            raise ValueError("persistent database path required")

        self._path = str(database_path)

        with self._connect() as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS product001_commercial_grants (
                    grant_id TEXT PRIMARY KEY,
                    definition TEXT NOT NULL,
                    revoked INTEGER NOT NULL DEFAULT 0
                        CHECK(revoked IN (0, 1))
                );

                CREATE TABLE IF NOT EXISTS product001_commercial_audit (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE,
                    grant_id TEXT NOT NULL
                        REFERENCES product001_commercial_grants(grant_id),
                    record TEXT NOT NULL
                );
            """)

    def _connect(self):
        connection = sqlite3.connect(
            self._path, timeout=5.0, isolation_level=None
        )
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("PRAGMA synchronous=FULL")
        except BaseException:
            connection.close()
            raise
        return connection

    @staticmethod
    def _event_id(value):
        if not isinstance(value, str):
            raise TypeError("event_id must be a string")
        if not value.strip():
            raise ValueError("event_id must not be empty")

    def _apply(self, *, event_id, grant, action):
        self._event_id(event_id)
        if not isinstance(grant, Product001CommercialApprovalGrant):
            raise TypeError("invalid commercial grant")

        definition = _json(asdict(grant))
        record = _json({
            "action": action,
            "event_id": event_id,
            "grant_id": grant.grant_id,
            "grant_definition": definition,
        })

        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")

            prior = connection.execute(
                "SELECT record FROM product001_commercial_audit "
                "WHERE event_id=?", (event_id,),
            ).fetchone()

            if prior is not None:
                if prior[0] != record:
                    raise CommercialApprovalStorageConflict(
                        "event_id conflict"
                    )
                connection.execute("COMMIT")
                return False

            existing = connection.execute(
                "SELECT definition, revoked "
                "FROM product001_commercial_grants WHERE grant_id=?",
                (grant.grant_id,),
            ).fetchone()

            if existing is not None and existing[0] != definition:
                raise CommercialApprovalStorageConflict(
                    "grant_id conflict"
                )

            if action == "REGISTER":
                if existing is not None:
                    if existing[1]:
                        raise CommercialApprovalStorageConflict(
                            "revoked grant cannot be reactivated"
                        )
                else:
                    connection.execute(
                        "INSERT INTO product001_commercial_grants "
                        "(grant_id, definition) VALUES (?, ?)",
                        (grant.grant_id, definition),
                    )
            elif action == "REVOKE":
                if existing is None:
                    raise CommercialApprovalStorageConflict(
                        "grant does not exist"
                    )
                if existing[1]:
                    raise CommercialApprovalStorageConflict(
                        "grant already revoked"
                    )
                connection.execute(
                    "UPDATE product001_commercial_grants "
                    "SET revoked=1 WHERE grant_id=?",
                    (grant.grant_id,),
                )
            else:
                raise ValueError("invalid administrative action")

            connection.execute(
                "INSERT INTO product001_commercial_audit "
                "(event_id, grant_id, record) VALUES (?, ?, ?)",
                (event_id, grant.grant_id, record),
            )
            connection.execute("COMMIT")
            return True
        except BaseException as error:
            if connection.in_transaction:
                try:
                    connection.execute("ROLLBACK")
                except BaseException as rollback_error:
                    error.add_note(
                        "Rollback failed: "
                        + type(rollback_error).__name__
                    )
            raise
        finally:
            connection.close()

    def register_grant(self, *, event_id, grant):
        return self._apply(
            event_id=event_id, grant=grant, action="REGISTER"
        )

    def revoke_grant(self, *, event_id, grant):
        return self._apply(
            event_id=event_id, grant=grant, action="REVOKE"
        )

    def read_grant(self, *, grant_id):
        if not isinstance(grant_id, str) or not grant_id.strip():
            raise ValueError("invalid grant_id")
        with self._connect() as connection:
            row = connection.execute(
                "SELECT definition, revoked "
                "FROM product001_commercial_grants WHERE grant_id=?",
                (grant_id,),
            ).fetchone()
        if row is None:
            return None
        return _restore_grant(row[0]), bool(row[1])

    def read_audit(self):
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT record FROM product001_commercial_audit "
                "ORDER BY sequence"
            ).fetchall()
        return tuple(json.loads(row[0]) for row in rows)
