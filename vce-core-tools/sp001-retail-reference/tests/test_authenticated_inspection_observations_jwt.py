import sqlite3
import time

import pytest

import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys
from test_retail_inspection_observation import observation
from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
    CaseAccessPermission,
)
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationIdentity as Identity,
)
from sp001.infrastructure.jwt_case_access_authenticator import (
    JwtCaseAccessAuthenticator,
)
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    SqliteAuthorizedInspectionObservations,
    InspectionObservationAuthenticationRejected as Rejected,
    InspectionObservationAccessDenied as Denied,
)
from sp001.services.authenticated_inspection_observations import (
    AuthenticatedInspectionObservations,
)


SAVE = Operation.SAVE_RETAIL_OBSERVATION
READ = Operation.READ_RETAIL_OBSERVATION
CASE = "CASE"
IDENTITY = Identity("OBS-1", 1)


class CountingAuthenticator:
    def __init__(self, delegate):
        self.delegate = delegate
        self.calls = 0

    def authenticate(self, *, credential):
        self.calls += 1
        return self.delegate.authenticate(credential=credential)


def environment(tmp_path, keys, operations=(SAVE, READ)):
    path = tmp_path / "observations.sqlite3"
    now = int(time.time())
    backend = SqliteAuthorizedInspectionObservations(
        database_path=path, expected_audience=jwt_setup.AUDIENCE,
        clock=lambda: int(time.time()),
    )
    auth = CountingAuthenticator(JwtCaseAccessAuthenticator(
        issuer=jwt_setup.ISSUER, audience=jwt_setup.AUDIENCE,
        public_keys={"KEY-1": keys[0].public_key()},
        max_lifetime_seconds=120, max_token_bytes=16384,
    ))
    service = AuthenticatedInspectionObservations(
        authenticator=auth, backend=backend,
        expected_audience=jwt_setup.AUDIENCE, clock=lambda: int(time.time()),
    )
    principal = AuthenticatedPrincipal(jwt_setup.ISSUER, "SUBJECT")
    grants = SqliteCaseAccessGrants(database_path=path)
    definitions = []
    for operation in operations:
        item = CaseAccessGrant(
            f"G-{operation.value}", principal,
            CaseAccessPermission(CASE, operation), now - 10, now + 600,
        )
        grants.apply(record=GrantAdministrationRecord(
            f"ADD-{operation.value}", principal, Action.GRANT, item, now,
        ))
        definitions.append(item)
    return path, service, auth, grants, definitions


def count(path):
    with sqlite3.connect(path) as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM retail_inspection_observations"
        ).fetchone()[0]


def test_signed_save_retry_read_and_absence(tmp_path, keys):
    path, service, auth, _, _ = environment(tmp_path, keys)
    item = observation(case_id=CASE)
    write = jwt_setup.token(keys[0], operations=(SAVE,))
    read = jwt_setup.token(keys[0], operations=(READ,))
    assert service.save(credential=write, observation=item) == item
    assert service.save(credential=write, observation=item) == item
    assert service.recover(
        credential=read, identity=IDENTITY, case_id=CASE,
    ) == item
    assert service.recover(
        credential=read, identity=Identity("ABSENT", 1), case_id=CASE,
    ) is None
    assert auth.calls == 4
    assert count(path) == 1


@pytest.mark.parametrize("fault", ["signature", "audience", "issuer", "expired"])
def test_invalid_signed_credentials_never_write(tmp_path, keys, fault):
    path, service, _, _, _ = environment(tmp_path, keys)
    overrides = {}
    if fault == "audience":
        overrides["aud"] = "OTHER"
    elif fault == "issuer":
        overrides["iss"] = "OTHER"
    elif fault == "expired":
        now = int(time.time())
        overrides.update(iat=now - 90, nbf=now - 90, exp=now - 1)
    token = jwt_setup.token(
        keys[1] if fault == "signature" else keys[0],
        operations=(SAVE,), overrides=overrides,
    )
    with pytest.raises(Rejected):
        service.save(credential=token, observation=observation(case_id=CASE))
    assert count(path) == 0


@pytest.mark.parametrize("operations", [
    (READ,), (Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT),
])
def test_wrong_claims_cannot_write(tmp_path, keys, operations):
    path, service, _, _, _ = environment(tmp_path, keys)
    with pytest.raises(Denied):
        service.save(
            credential=jwt_setup.token(keys[0], operations=operations),
            observation=observation(case_id=CASE),
        )
    assert count(path) == 0


def test_valid_token_does_not_replace_local_grant(tmp_path, keys):
    path, service, _, _, _ = environment(tmp_path, keys, operations=())
    with pytest.raises(Denied):
        service.save(
            credential=jwt_setup.token(keys[0], operations=(SAVE,)),
            observation=observation(case_id=CASE),
        )
    assert count(path) == 0


def test_local_revocation_blocks_retry_and_recovery_with_same_tokens(tmp_path, keys):
    path, service, auth, grants, definitions = environment(tmp_path, keys)
    write = jwt_setup.token(keys[0], operations=(SAVE,))
    read = jwt_setup.token(keys[0], operations=(READ,))
    item = observation(case_id=CASE)
    service.save(credential=write, observation=item)
    for definition in definitions:
        grants.apply(record=GrantAdministrationRecord(
            f"REVOKE-{definition.grant_id}", definition.principal,
            Action.REVOKE, definition, int(time.time()),
        ))
    with pytest.raises(Denied):
        service.save(credential=write, observation=item)
    with pytest.raises(Denied):
        service.recover(credential=read, identity=IDENTITY, case_id=CASE)
    assert auth.calls == 3
    assert count(path) == 1


def test_other_signed_subject_has_no_implicit_local_grant(tmp_path, keys):
    path, service, _, _, _ = environment(tmp_path, keys)
    credential = jwt_setup.token(
        keys[0], operations=(SAVE,), overrides={"sub": "OTHER"},
    )
    with pytest.raises(Denied):
        service.save(credential=credential, observation=observation(case_id=CASE))
    assert count(path) == 0
