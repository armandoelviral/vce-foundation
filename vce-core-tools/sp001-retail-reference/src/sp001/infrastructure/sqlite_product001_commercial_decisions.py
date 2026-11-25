"""Internal transactional decision writer; authentication is external."""

from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path
import json
import sqlite3

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.product001_commercial_approval_decision import (
    Product001CommercialApprovalDecision,
)
from sp001.contracts.product001_commercial_approval_grant import (
    Product001CommercialApprovalOperation,
)
from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentCertificateV1,
    commitment_certificate_digest,
)
from sp001.infrastructure.sqlite_product001_commercial_approval import (
    SqliteProduct001CommercialApproval,
    _restore_grant,
)
from sp001.services.product001_commercial_approval_scope import (
    commercial_scope_covers,
)


class CommercialDecisionDenied(PermissionError):
    pass


class CommercialDecisionConflict(ValueError):
    pass


def _canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


class SqliteProduct001CommercialDecisionWriter:
    """Trusted internal writer; principal must come from authentication."""

    def __init__(
        self, *, database_path: str | Path,
        clock: Callable[[], int],
    ):
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._clock = clock
        self._grants = SqliteProduct001CommercialApproval(
            database_path=database_path
        )
        self._path = str(database_path)

        connection = self._connect()
        try:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS product001_commercial_decisions (
                    decision_id TEXT PRIMARY KEY,
                    grant_id TEXT NOT NULL
                        REFERENCES product001_commercial_grants(grant_id),
                    definition TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS product001_commercial_decision_audit (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    decision_id TEXT NOT NULL UNIQUE
                        REFERENCES product001_commercial_decisions(decision_id),
                    record TEXT NOT NULL
                );
            """)
        finally:
            connection.close()

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

    def save_decision(
        self, *, decision: Product001CommercialApprovalDecision,
        authenticated_principal: AuthenticatedPrincipal,
        before_commit: Callable[[], None] | None = None,
        commitment: CommitmentCertificateV1 | None = None,
    ) -> bool:
        if not isinstance(
            decision, Product001CommercialApprovalDecision
        ):
            raise TypeError("invalid commercial decision")
        if not isinstance(
            authenticated_principal, AuthenticatedPrincipal
        ):
            raise TypeError("invalid authenticated principal")

        if before_commit is not None and not callable(before_commit):
            raise TypeError("before_commit must be callable")

        definition = _canonical(asdict(decision))
        audit_record = {
            "action": "RECORD_DECISION",
            "decision_id": decision.decision_id,
            "grant_id": decision.authorization_grant_id,
            "definition": definition,
        }
        if commitment is not None:
            if type(commitment) is not CommitmentCertificateV1:
                raise TypeError("invalid commitment certificate")
            context = commitment.context
            if (
                context.operation_id != decision.decision_id
                or context.organization_id != decision.document_scope.organization_id
            ):
                raise CommercialDecisionConflict("commitment identity does not match decision")
            audit_record["commitment"] = {
                "version": 1,
                "certificate_digest": commitment_certificate_digest(commitment),
                "context": asdict(context),
            }
        audit = _canonical(audit_record)

        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")

            now = self._clock()
            if type(now) is not int or now < 0:
                raise ValueError(
                    "clock must return nonnegative integer Unix seconds"
                )

            row = connection.execute(
                "SELECT definition, revoked "
                "FROM product001_commercial_grants WHERE grant_id=?",
                (decision.authorization_grant_id,),
            ).fetchone()

            if row is None or row[1] != 0:
                raise CommercialDecisionDenied(
                    "missing or revoked grant"
                )

            try:
                grant = _restore_grant(row[0])
            except (ValueError, TypeError, KeyError) as exc:
                raise CommercialDecisionDenied(
                    "invalid stored grant"
                ) from exc

            if (
                grant.grant_id != decision.authorization_grant_id
                or grant.principal != authenticated_principal
                or decision.principal != authenticated_principal
                or grant.operation is not (
                    Product001CommercialApprovalOperation
                    .APPROVE_PLANOGRAM_VERSION
                )
                or not (grant.valid_from <= now < grant.expires_at)
                or not commercial_scope_covers(
                    grant.scope, decision.document_scope
                )
            ):
                raise CommercialDecisionDenied(
                    "commercial authorization rejected"
                )

            # A broad document scope must not authorize a POS
            # outside an explicit grant, even if its own scope is ALL.
            pos = decision.version_binding.point_of_sale_id
            from sp001.contracts.knowledge_source_scope import (
                KnowledgeScopeMode,
            )
            grant_pos = grant.scope.point_of_sale_scope
            if (
                grant_pos.mode is KnowledgeScopeMode.EXPLICIT
                and pos not in grant_pos.ids
            ):
                raise CommercialDecisionDenied(
                    "bound POS outside grant"
                )

            existing = connection.execute(
                "SELECT definition FROM product001_commercial_decisions "
                "WHERE decision_id=?",
                (decision.decision_id,),
            ).fetchone()

            if existing is not None:
                if existing[0] != definition:
                    raise CommercialDecisionConflict(
                        "decision_id conflict"
                    )
                audit_row = connection.execute(
                    "SELECT record "
                    "FROM product001_commercial_decision_audit "
                    "WHERE decision_id=?",
                    (decision.decision_id,),
                ).fetchone()
                if audit_row is None or audit_row[0] != audit:
                    raise CommercialDecisionConflict(
                        "missing or inconsistent decision audit"
                    )
                if before_commit is not None:
                    before_commit()
                connection.execute("COMMIT")
                return False

            connection.execute(
                "INSERT INTO product001_commercial_decisions "
                "(decision_id, grant_id, definition) VALUES (?, ?, ?)",
                (
                    decision.decision_id,
                    decision.authorization_grant_id,
                    definition,
                ),
            )
            connection.execute(
                "INSERT INTO product001_commercial_decision_audit "
                "(decision_id, record) VALUES (?, ?)",
                (decision.decision_id, audit),
            )
            if before_commit is not None:
                before_commit()
            connection.execute("COMMIT")
            return True
        except BaseException:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            raise
        finally:
            connection.close()
