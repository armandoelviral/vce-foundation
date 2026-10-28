import sqlite3
from dataclasses import replace

import pytest

from test_retail_inspection_observation import observation
from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
    CaseAccessPermission as Permission,
    ValidatedCaseAccessContext,
)
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict as Conflict,
    RetailInspectionObservationIdentity as Identity,
    StoredRetailInspectionObservation as Stored,
)
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.infrastructure.sqlite_retail_inspection_observations import (
    SqliteRetailInspectionObservationStore,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    SqliteAuthorizedInspectionObservations as Backend,
    InspectionObservationAccessDenied as Denied,
    InspectionObservationAuthenticationRejected as Rejected,
)


SAVE = Operation.SAVE_RETAIL_OBSERVATION
READ = Operation.READ_RETAIL_OBSERVATION


def environment(tmp_path):
    path = tmp_path / "shared.sqlite3"
    now = [150]
    backend = Backend(
        database_path=path, expected_audience="OBS",
        clock=lambda: now[0],
    )
    principal = AuthenticatedPrincipal("ISSUER", "SUBJECT")
    grants = SqliteCaseAccessGrants(database_path=path)
    return path, now, backend, principal, grants


def access(principal, *operations, case_id="CASE-1"):
    return ValidatedCaseAccessContext(
        principal, "OBS", 100, 100, 300,
        tuple(Permission(case_id, operation) for operation in operations),
    )


def grant(grants, principal, operation, *, case_id="CASE-1", expires_at=250):
    item = CaseAccessGrant(
        f"G-{case_id}-{operation.value}", principal,
        Permission(case_id, operation), 100, expires_at,
    )
    grants.apply(record=GrantAdministrationRecord(
        f"ADD-{item.grant_id}", principal, Action.GRANT, item, 100,
    ))
    return item


def key(item):
    return Identity(item.observation_id, item.observation_version)


def recover(backend, context, item, case_id="CASE-1"):
    return backend.recover_authorized(
        access=context, identity=key(item), case_id=case_id,
    )


def count(path):
    with sqlite3.connect(path) as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM retail_inspection_observations"
        ).fetchone()[0]


def test_save_only_and_read_only_are_independent_and_reopen(tmp_path):
    path, now, backend, principal, grants = environment(tmp_path)
    grant(grants, principal, SAVE)
    grant(grants, principal, READ)
    item = observation()
    assert backend.save_authorized(
        access=access(principal, SAVE), observation=item,
    ) == item
    assert backend.save_authorized(
        access=access(principal, SAVE), observation=item,
    ) == item
    with pytest.raises(Denied):
        recover(backend, access(principal, SAVE), item)
    with pytest.raises(Denied):
        backend.save_authorized(access=access(principal, READ), observation=item)
    reopened = Backend(
        database_path=path, expected_audience="OBS", clock=lambda: now[0],
    )
    assert recover(reopened, access(principal, READ), item) == item
    assert count(path) == 1


@pytest.mark.parametrize("fault", [
    "no_claim", "no_grant", "other_case", "other_principal", "report_permissions",
])
def test_denied_save_never_inserts(tmp_path, fault):
    path, _, backend, principal, grants = environment(tmp_path)
    ctx = access(principal, SAVE)
    if fault == "no_claim":
        grant(grants, principal, SAVE)
        ctx = access(principal)
    elif fault == "other_case":
        grant(grants, principal, SAVE, case_id="OTHER")
    elif fault == "other_principal":
        grant(grants, AuthenticatedPrincipal("ISSUER", "OTHER"), SAVE)
    elif fault == "report_permissions":
        for operation in (Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT):
            grant(grants, principal, operation)
        ctx = access(
            principal, Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT,
        )
    with pytest.raises(Denied):
        backend.save_authorized(access=ctx, observation=observation())
    assert count(path) == 0


def test_revocation_blocks_retry_and_recovery_preserving_original(tmp_path):
    path, _, backend, principal, grants = environment(tmp_path)
    definitions = [grant(grants, principal, operation) for operation in (SAVE, READ)]
    item = observation()
    ctx = access(principal, SAVE, READ)
    backend.save_authorized(access=ctx, observation=item)
    for definition in definitions:
        grants.apply(record=GrantAdministrationRecord(
            f"REVOKE-{definition.grant_id}", principal,
            Action.REVOKE, definition, 150,
        ))
    with pytest.raises(Denied):
        backend.save_authorized(access=ctx, observation=item)
    with pytest.raises(Denied):
        recover(backend, ctx, item)
    stored = SqliteRetailInspectionObservationStore(database_path=path).get(
        identity=key(item),
    )
    assert stored.document == serialize(item)
    assert count(path) == 1


def test_authorized_absence_and_wrong_case(tmp_path):
    _, _, backend, principal, grants = environment(tmp_path)
    grant(grants, principal, SAVE)
    grant(grants, principal, READ)
    grant(grants, principal, READ, case_id="OTHER")
    item = observation()
    assert recover(backend, access(principal, READ), item) is None
    backend.save_authorized(access=access(principal, SAVE), observation=item)
    with pytest.raises(Denied):
        recover(
            backend, access(principal, READ, case_id="OTHER"), item,
            case_id="OTHER",
        )
    with pytest.raises(Denied):
        recover(backend, access(principal), item)


def test_conflict_and_correction_preserve_original(tmp_path):
    path, _, backend, principal, grants = environment(tmp_path)
    grant(grants, principal, SAVE)
    ctx = access(principal, SAVE)
    item = observation()
    backend.save_authorized(access=ctx, observation=item)
    changed = replace(item, description="Different description.")
    with pytest.raises(Conflict):
        backend.save_authorized(access=ctx, observation=changed)
    backend.save_authorized(
        access=ctx, observation=replace(changed, observation_version=2),
    )
    assert count(path) == 2
    stored = SqliteRetailInspectionObservationStore(database_path=path).get(
        identity=key(item),
    )
    assert stored.document == serialize(item)


@pytest.mark.parametrize("fault", ["audience", "expired", "not_yet_valid"])
def test_unusable_context_cannot_write(tmp_path, fault):
    path, now, backend, principal, grants = environment(tmp_path)
    grant(grants, principal, SAVE)
    ctx = access(principal, SAVE)
    if fault == "audience":
        ctx = replace(ctx, audience="OTHER")
    else:
        now[0] = 300 if fault == "expired" else 99
    with pytest.raises(Rejected):
        backend.save_authorized(access=ctx, observation=observation())
    assert count(path) == 0


@pytest.mark.parametrize("operation", ["save", "recover"])
@pytest.mark.parametrize("expiry", ["token", "grant"])
def test_expiration_before_completion_rejects_current_operation(
    tmp_path, operation, expiry,
):
    path, _, _, principal, grants = environment(tmp_path)
    for permission in (SAVE, READ):
        grant(grants, principal, permission, expires_at=200 if expiry == "grant" else 250)
    item = observation()
    store = SqliteRetailInspectionObservationStore(database_path=path)
    if operation == "recover":
        store.put(observation=Stored(key(item), serialize(item)))
    before = count(path)
    times = iter([150, 200])
    backend = Backend(
        database_path=path, expected_audience="OBS", clock=lambda: next(times),
    )
    ctx = access(principal, SAVE, READ)
    if expiry == "token":
        ctx = replace(ctx, expires_at=200)
    with pytest.raises(Rejected if expiry == "token" else Denied):
        if operation == "save":
            backend.save_authorized(access=ctx, observation=item)
        else:
            recover(backend, ctx, item)
    assert count(path) == before


def test_storage_failure_propagates_instead_of_absence(tmp_path):
    path, _, backend, principal, grants = environment(tmp_path)
    grant(grants, principal, READ)
    with sqlite3.connect(path) as connection:
        connection.execute("DROP TABLE retail_inspection_observations")
    with pytest.raises(sqlite3.OperationalError):
        recover(backend, access(principal, READ), observation())
