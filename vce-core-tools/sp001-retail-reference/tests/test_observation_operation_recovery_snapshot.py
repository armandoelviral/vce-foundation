import sqlite3
from dataclasses import replace

import pytest

import test_sqlite_authorized_inspection_observations as setup
from test_observation_operation_recovery import prepared
from sp001.infrastructure.sqlite_observation_operations import (
    ObservationOperationIntegrityFailure,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


class ReceiptCursor:
    def __init__(self, cursor, callback):
        self.cursor = cursor
        self.callback = callback

    def fetchone(self):
        row = self.cursor.fetchone()
        self.callback()
        return row

    def __getattr__(self, name):
        return getattr(self.cursor, name)


class ObservedConnection:
    def __init__(self, connection, callback):
        self.connection = connection
        self.callback = callback
        self.armed = True

    def execute(self, sql, *args, **kwargs):
        cursor = self.connection.execute(sql, *args, **kwargs)
        normalized = " ".join(sql.upper().split())
        if (
            self.armed
            and normalized.startswith("SELECT ")
            and "FROM RETAIL_OBSERVATION_OPERATIONS" in normalized
        ):
            self.armed = False

            def after_receipt():
                assert self.connection.in_transaction
                self.callback()

            return ReceiptCursor(cursor, after_receipt)
        return cursor

    def __getattr__(self, name):
        return getattr(self.connection, name)


def intercept_receipt(monkeypatch, backend, callback):
    original = backend._connect
    monkeypatch.setattr(
        backend, "_connect",
        lambda: ObservedConnection(original(), callback),
    )


def test_effect_changed_after_receipt_is_visible_only_next_query(
    tmp_path, monkeypatch,
):
    path, backend, access, request, receipt = prepared(tmp_path)
    changed = serialize(replace(
        request.observation, description="Privileged concurrent alteration.",
    ))
    commits = []

    def alter_from_second_connection():
        with sqlite3.connect(path, timeout=5) as writer:
            writer.execute(
                "UPDATE retail_inspection_observations SET document=?",
                (changed,),
            )
            writer.commit()
        commits.append("committed")

    with monkeypatch.context() as patch:
        intercept_receipt(patch, backend, alter_from_second_connection)
        recovered = backend.recover_operation_authorized(
            access=access, identity=receipt.operation,
        )

    assert commits == ["committed"]
    assert recovered == receipt
    with sqlite3.connect(path) as connection:
        assert connection.execute(
            "SELECT document FROM retail_inspection_observations"
        ).fetchone()[0] == changed

    # The next snapshot sees the contradiction instead of mixing snapshots.
    with pytest.raises(ObservationOperationIntegrityFailure):
        backend.recover_operation_authorized(
            access=access, identity=receipt.operation,
        )


def test_revocation_after_snapshot_blocks_next_query(tmp_path, monkeypatch):
    path, backend, access, _, receipt = prepared(tmp_path)
    grants = setup.SqliteCaseAccessGrants(database_path=path)
    definition = setup.grant(grants, access.principal, setup.READ)
    commits = []

    def revoke_from_second_connection():
        assert grants.apply(record=setup.GrantAdministrationRecord(
            "SNAPSHOT-REVOKE", access.principal,
            setup.Action.REVOKE, definition, 150,
        ))
        commits.append("committed")

    with monkeypatch.context() as patch:
        intercept_receipt(patch, backend, revoke_from_second_connection)
        assert backend.recover_operation_authorized(
            access=access, identity=receipt.operation,
        ) == receipt

    assert commits == ["committed"]
    assert grants.permits(
        principal=access.principal,
        permission=definition.permission,
        at_time=150,
    ) is False
    with pytest.raises(setup.Denied):
        backend.recover_operation_authorized(
            access=access, identity=receipt.operation,
        )


def test_expiration_before_return_rejects_current_result(tmp_path, monkeypatch):
    path, backend, access, _, receipt = prepared(tmp_path)
    now = [150]
    backend._clock = lambda: now[0]

    def expire_after_receipt():
        now[0] = access.expires_at

    with monkeypatch.context() as patch:
        intercept_receipt(patch, backend, expire_after_receipt)
        with pytest.raises(setup.Rejected):
            backend.recover_operation_authorized(
                access=access, identity=receipt.operation,
            )

    # Rejection does not remove the already committed pair.
    with sqlite3.connect(path) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM retail_observation_operations"
        ).fetchone()[0] == 1
        assert connection.execute(
            "SELECT COUNT(*) FROM retail_inspection_observations"
        ).fetchone()[0] == 1

    now[0] = 150  # Restore the synthetic test clock only.
    assert backend.recover_operation_authorized(
        access=access, identity=receipt.operation,
    ) == receipt
