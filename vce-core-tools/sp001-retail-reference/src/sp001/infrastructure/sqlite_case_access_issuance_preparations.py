from dataclasses import asdict
import json

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import CaseAccessOperation, CaseAccessPermission
from sp001.contracts.case_access_grant_snapshot import CaseAccessGrantSnapshot
from sp001.contracts.case_access_issuance_preparation import (
    FederatedPrincipalBinding, CaseAccessTokenPayload,
    IssuanceGrantReference, CaseAccessIssuancePreparation,
)
from sp001.contracts.federated_principal_binding_snapshot import (
    FederatedPrincipalBindingSnapshot,
)
from sp001.infrastructure.sqlite_case_access_grants import (
    SqliteCaseAccessGrants, _grant,
)
from sp001.services.case_access_issuance_reference_validation import (
    validate_issuance_references,
)


def _serialize(value):
    return json.dumps(asdict(value), sort_keys=True, separators=(",", ":"))


def _binding(value):
    return FederatedPrincipalBinding(
        binding_id=value["binding_id"], revision=value["revision"],
        external_principal=AuthenticatedPrincipal(**value["external_principal"]),
        internal_subject=value["internal_subject"],
    )


def _preparation(document):
    value = json.loads(document)
    payload = value["payload"]
    permissions = tuple(CaseAccessPermission(
        item["case_id"], CaseAccessOperation(item["operation"])
    ) for item in payload["permissions"])
    return CaseAccessIssuancePreparation(
        request_id=value["request_id"],
        binding=_binding(value["binding"]),
        payload=CaseAccessTokenPayload(
            **{key: item for key, item in payload.items() if key != "permissions"},
            permissions=permissions,
        ),
        signing_key_id=value["signing_key_id"],
        grant_references=tuple(IssuanceGrantReference(
            grant_id=item["grant_id"], revision=item["revision"],
            expires_at=item["expires_at"],
            permission=CaseAccessPermission(
                item["permission"]["case_id"],
                CaseAccessOperation(item["permission"]["operation"]),
            ),
        ) for item in value["grant_references"]),
    )


class SqliteCaseAccessIssuancePreparations(SqliteCaseAccessGrants):
    """Trusted storage; binding administration requires an external authority gate."""

    def __init__(self, *, database_path):
        super().__init__(database_path=database_path)
        with self._connection() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS federated_principal_bindings (
                    binding_id TEXT PRIMARY KEY,
                    revision INTEGER NOT NULL CHECK(revision>=1),
                    external_issuer TEXT NOT NULL,
                    external_subject TEXT NOT NULL,
                    document TEXT NOT NULL,
                    UNIQUE(external_issuer, external_subject)
                );
                CREATE TABLE IF NOT EXISTS federated_binding_history (
                    binding_id TEXT NOT NULL,
                    revision INTEGER NOT NULL,
                    document TEXT NOT NULL,
                    PRIMARY KEY(binding_id, revision)
                );
                CREATE TABLE IF NOT EXISTS case_access_issuance_preparations (
                    request_id TEXT PRIMARY KEY,
                    token_id TEXT NOT NULL UNIQUE,
                    status TEXT NOT NULL CHECK(status='PREPARED'),
                    document TEXT NOT NULL
                );
            """)

    def put_binding(self, *, snapshot: FederatedPrincipalBindingSnapshot,
                    expected_revision: int | None) -> bool:
        if not isinstance(snapshot, FederatedPrincipalBindingSnapshot):
            raise TypeError("snapshot must be a FederatedPrincipalBindingSnapshot")
        if expected_revision is not None and (
            isinstance(expected_revision, bool)
            or not isinstance(expected_revision, int)
            or expected_revision < 1
        ):
            raise ValueError("expected_revision must be positive or None")
        binding = snapshot.binding
        required = 1 if expected_revision is None else expected_revision + 1
        if binding.revision != required:
            raise ValueError("binding revision must be the exact successor")
        document = _serialize(snapshot)
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute(
                    "SELECT revision, document FROM federated_principal_bindings WHERE binding_id=?",
                    (binding.binding_id,),
                ).fetchone()
                if row is not None and row[1] == document:
                    connection.commit()
                    return True
                if (
                    (expected_revision is None and row is not None)
                    or (expected_revision is not None and (
                        row is None or row[0] != expected_revision
                    ))
                ):
                    connection.rollback()
                    return False
                values = (
                    binding.revision, binding.external_principal.issuer,
                    binding.external_principal.subject, document, binding.binding_id,
                )
                if row is None:
                    connection.execute(
                        """INSERT INTO federated_principal_bindings
                        (revision, external_issuer, external_subject, document, binding_id)
                        VALUES (?, ?, ?, ?, ?)""", values,
                    )
                else:
                    connection.execute(
                        """UPDATE federated_principal_bindings SET
                        revision=?, external_issuer=?, external_subject=?, document=?
                        WHERE binding_id=?""", values,
                    )
                connection.execute(
                    "INSERT INTO federated_binding_history VALUES (?, ?, ?)",
                    (binding.binding_id, binding.revision, document),
                )
                connection.commit()
                return True
            except BaseException:
                connection.rollback()
                raise

    def prepare(self, *, preparation: CaseAccessIssuancePreparation,
                at_time: int) -> CaseAccessIssuancePreparation:
        if not isinstance(preparation, CaseAccessIssuancePreparation):
            raise TypeError("preparation must be a CaseAccessIssuancePreparation")
        document = _serialize(preparation)
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                existing = connection.execute(
                    "SELECT document FROM case_access_issuance_preparations WHERE request_id=?",
                    (preparation.request_id,),
                ).fetchone()
                if existing is not None and existing[0] != document:
                    raise ValueError("request_id conflicts with prepared issuance")

                self._validate_references(
                    connection=connection, preparation=preparation,
                    at_time=at_time,
                )
                if existing is None:
                    connection.execute(
                        """INSERT INTO case_access_issuance_preparations
                        (request_id, token_id, status, document)
                        VALUES (?, ?, 'PREPARED', ?)""",
                        (preparation.request_id, preparation.payload.token_id, document),
                    )
                connection.commit()
                return preparation
            except BaseException:
                connection.rollback()
                raise

    def read_prepared(self, *, request_id: str):
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("request_id must be a nonempty string")
        with self._connection() as connection:
            row = connection.execute(
                "SELECT document FROM case_access_issuance_preparations WHERE request_id=?",
                (request_id,),
            ).fetchone()
        return None if row is None else _preparation(row[0])

    def _validate_references(self, *, connection, preparation, at_time):
        row = connection.execute(
            "SELECT document FROM federated_principal_bindings WHERE binding_id=?",
            (preparation.binding.binding_id,),
        ).fetchone()
        binding_snapshot = None
        if row is not None:
            value = json.loads(row[0])
            binding_snapshot = FederatedPrincipalBindingSnapshot(
                binding=_binding(value["binding"]), active=value["active"],
            )
        snapshots = []
        for reference in preparation.grant_references:
            row = connection.execute(
                """SELECT g.definition, g.revoked,
                (SELECT COUNT(*) FROM case_access_grant_audit AS a
                 WHERE a.grant_id=g.grant_id)
                FROM case_access_grants AS g WHERE g.grant_id=?""",
                (reference.grant_id,),
            ).fetchone()
            if row is not None:
                if row[1] not in (0, 1):
                    raise ValueError("invalid persisted revocation state")
                snapshots.append(CaseAccessGrantSnapshot(
                    grant=_grant(json.loads(row[0])),
                    revision=row[2], revoked=bool(row[1]),
                ))
        validate_issuance_references(
            preparation=preparation,
            binding_snapshot=binding_snapshot,
            grant_snapshots=tuple(snapshots), at_time=at_time,
        )
