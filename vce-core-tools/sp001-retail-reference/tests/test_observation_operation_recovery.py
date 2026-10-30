import sqlite3
from dataclasses import replace

import pytest

import test_sqlite_authorized_inspection_observations as setup
from test_sqlite_observation_operations import environment
from sp001.contracts.retail_observation_operation import (
    RetailObservationSaveRequest as Request,
    RetailObservationOperationIdentity as Identity,
    RetailObservationEffectDisposition as Disposition,
)
from sp001.infrastructure.sqlite_observation_operations import (
    SqliteObservationOperations as Backend,
    ObservationOperationIntegrityFailure as IntegrityFailure,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    deserialize_retail_inspection_observation as deserialize,
    serialize_retail_inspection_observation as serialize,
)


def prepared(tmp_path):
    path, backend, write_access = environment(tmp_path)
    principal = write_access.principal
    grants = setup.SqliteCaseAccessGrants(database_path=path)
    setup.grant(grants, principal, setup.READ)
    request = Request("REQUEST", setup.observation())
    receipt = backend.save_operation_authorized(
        access=write_access, request=request,
    )
    return path, backend, setup.access(principal, setup.READ), request, receipt


@pytest.mark.parametrize("reused", [False, True])
def test_reopens_and_recovers_exact_pair(tmp_path, reused):
    path, backend, access, request, original = prepared(tmp_path)
    if reused:
        original = backend.save_operation_authorized(
            access=setup.access(access.principal, setup.SAVE),
            request=replace(request, request_id="SECOND"),
        )
    reopened = Backend(
        database_path=path, expected_audience="OBS", clock=lambda: 150,
    )
    recovered = reopened.recover_operation_authorized(
        access=access, identity=original.operation,
    )
    assert recovered == original
    assert deserialize(recovered.stored_observation.document) == request.observation
    assert recovered.disposition is (
        Disposition.REUSED if reused else Disposition.CREATED
    )


def test_authorized_absence_does_not_mean_rejected(tmp_path):
    _, backend, access, _, receipt = prepared(tmp_path)
    missing = replace(receipt.operation, request_id="MISSING")
    assert backend.recover_operation_authorized(
        access=access, identity=missing,
    ) is None


def test_save_permission_does_not_grant_operation_read(tmp_path):
    _, backend, access, _, receipt = prepared(tmp_path)
    with pytest.raises(setup.Denied):
        backend.recover_operation_authorized(
            access=setup.access(access.principal, setup.SAVE),
            identity=replace(receipt.operation, request_id="MISSING"),
        )


def test_another_principal_cannot_read_receipt(tmp_path):
    _, backend, access, _, receipt = prepared(tmp_path)
    other = setup.AuthenticatedPrincipal("ISSUER", "OTHER")
    with pytest.raises(setup.Denied):
        backend.recover_operation_authorized(
            access=setup.access(other, setup.READ),
            identity=receipt.operation,
        )


@pytest.mark.parametrize("fault", [
    "missing_effect", "changed_effect", "invalid_receipt",
    "receipt_key", "receipt_case", "receipt_version",
])
def test_recovered_inconsistency_is_not_absence(tmp_path, fault):
    path, backend, access, request, receipt = prepared(tmp_path)
    with sqlite3.connect(path) as connection:
        if fault == "missing_effect":
            connection.execute("DELETE FROM retail_inspection_observations")
        elif fault == "changed_effect":
            changed = replace(request.observation, description="Changed.")
            connection.execute(
                "UPDATE retail_inspection_observations SET document=?",
                (serialize(changed),),
            )
        elif fault == "invalid_receipt":
            connection.execute(
                "UPDATE retail_observation_operations SET document='{}'"
            )
        elif fault == "receipt_key":
            connection.execute(
                "UPDATE retail_observation_operations SET observation_id='OTHER'"
            )
        elif fault == "receipt_case":
            changed = replace(request.observation, case_id="OTHER")
            connection.execute(
                "UPDATE retail_observation_operations SET document=?",
                (serialize(changed),),
            )
        else:
            connection.execute(
                "UPDATE retail_observation_operations SET observation_version='01'"
            )
    with pytest.raises(IntegrityFailure):
        backend.recover_operation_authorized(
            access=access, identity=receipt.operation,
        )


def test_revoked_read_blocks_recovery_without_deleting_effect(tmp_path):
    path, backend, access, _, receipt = prepared(tmp_path)
    grants = setup.SqliteCaseAccessGrants(database_path=path)
    definition = setup.grant(grants, access.principal, setup.READ)
    grants.apply(record=setup.GrantAdministrationRecord(
        "REVOKE-READ", access.principal, setup.Action.REVOKE, definition, 150,
    ))
    with pytest.raises(setup.Denied):
        backend.recover_operation_authorized(
            access=access, identity=receipt.operation,
        )
    with sqlite3.connect(path) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM retail_inspection_observations"
        ).fetchone()[0] == 1


def test_database_failure_propagates(tmp_path, monkeypatch):
    _, backend, access, _, receipt = prepared(tmp_path)

    def unavailable():
        raise sqlite3.OperationalError("synthetic unavailable database")

    monkeypatch.setattr(backend, "_connect", unavailable)
    with pytest.raises(sqlite3.OperationalError):
        backend.recover_operation_authorized(
            access=access, identity=receipt.operation,
        )


@pytest.mark.parametrize("name", ["access", "identity"])
def test_recovery_requires_nominal_inputs(tmp_path, name):
    _, backend, access, _, receipt = prepared(tmp_path)
    args = dict(access=access, identity=receipt.operation)
    args[name] = None
    with pytest.raises(TypeError):
        backend.recover_operation_authorized(**args)
