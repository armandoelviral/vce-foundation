import time

import pytest
from fastapi.testclient import TestClient

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys

from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
)
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)
from sp001.infrastructure.inspection_observation_read_http_host import (
    create_inspection_observation_read_app,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


ROUTE = "/v1/cases/CASE/inspection-observations/OBS-1/versions/1"


def headers(credential):
    return {"Authorization": f"Bearer {credential}"}


def prepare(tmp_path, keys):
    path, service, auth, grants, definitions = setup.environment(tmp_path, keys)
    item = setup.observation(case_id=setup.CASE)
    service.save(
        credential=jwt_setup.token(keys[0], operations=(setup.SAVE,)),
        observation=item,
    )
    app = create_inspection_observation_read_app(service=service)
    return path, service, auth, grants, definitions, item, app


def test_authorized_http_read_recovers_exact_document(tmp_path, keys):
    _, _, auth, _, _, item, app = prepare(tmp_path, keys)
    before = auth.calls
    credential = jwt_setup.token(keys[0], operations=(setup.READ,))

    with TestClient(app) as client:
        result = client.get(ROUTE, headers=headers(credential))

    assert result.status_code == 200
    assert result.json() == {
        "status": "ok",
        "observation_document": serialize(item),
    }
    assert result.headers["cache-control"] == "no-store"
    assert auth.calls == before + 2
    assert credential not in result.text


@pytest.mark.parametrize("fault", [
    "signature", "audience", "issuer", "expired",
])
def test_invalid_signed_credential_returns_no_observation(tmp_path, keys, fault):
    path, _, _, _, _, item, app = prepare(tmp_path, keys)
    overrides = {}
    if fault == "audience":
        overrides["aud"] = "OTHER"
    elif fault == "issuer":
        overrides["iss"] = "OTHER"
    elif fault == "expired":
        now = int(time.time())
        overrides.update(iat=now - 90, nbf=now - 90, exp=now - 1)

    credential = jwt_setup.token(
        keys[1] if fault == "signature" else keys[0],
        operations=(setup.READ,), overrides=overrides,
    )
    with TestClient(app) as client:
        result = client.get(ROUTE, headers=headers(credential))

    assert result.status_code == 401
    assert result.json() == {"status": "credential_rejected"}
    assert result.headers["cache-control"] == "no-store"
    assert item.description not in result.text
    assert credential not in result.text
    assert setup.count(path) == 1


@pytest.mark.parametrize("operations", [
    (),
    (Operation.SAVE_RETAIL_OBSERVATION,),
    (Operation.READ_RETAIL_REPORT,),
    (Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT),
])
def test_insufficient_claims_return_denial(tmp_path, keys, operations):
    _, _, _, _, _, item, app = prepare(tmp_path, keys)
    credential = jwt_setup.token(keys[0], operations=operations)
    with TestClient(app) as client:
        result = client.get(ROUTE, headers=headers(credential))
    assert result.status_code == 403
    assert result.json() == {"status": "access_denied"}
    assert item.description not in result.text


def test_valid_read_claim_without_local_read_grant_is_denied(tmp_path, keys):
    _, service, _, _, _ = setup.environment(
        tmp_path, keys, operations=(setup.SAVE,),
    )
    item = setup.observation(case_id=setup.CASE)
    service.save(
        credential=jwt_setup.token(keys[0], operations=(setup.SAVE,)),
        observation=item,
    )
    app = create_inspection_observation_read_app(service=service)
    credential = jwt_setup.token(keys[0], operations=(setup.READ,))
    with TestClient(app) as client:
        result = client.get(ROUTE, headers=headers(credential))
    assert result.status_code == 403
    assert result.json() == {"status": "access_denied"}


def test_absence_is_reported_only_after_authorized_lookup(tmp_path, keys):
    _, _, _, _, _, _, app = prepare(tmp_path, keys)
    missing_route = ROUTE.replace("OBS-1", "MISSING")
    read = jwt_setup.token(keys[0], operations=(setup.READ,))
    save_only = jwt_setup.token(keys[0], operations=(setup.SAVE,))

    with TestClient(app) as client:
        absent = client.get(missing_route, headers=headers(read))
        denied = client.get(missing_route, headers=headers(save_only))
        rejected = client.get(missing_route)

    assert absent.status_code == 404
    assert absent.json() == {"status": "observation_not_found"}
    assert denied.status_code == 403
    assert denied.json() == {"status": "access_denied"}
    assert rejected.status_code == 401
    assert rejected.json() == {"status": "credential_rejected"}


def test_same_token_is_denied_after_local_revocation(tmp_path, keys):
    path, _, _, grants, definitions, item, app = prepare(tmp_path, keys)
    credential = jwt_setup.token(keys[0], operations=(setup.READ,))
    read_grant = next(
        definition for definition in definitions
        if definition.permission.operation is setup.READ
    )

    with TestClient(app) as client:
        first = client.get(ROUTE, headers=headers(credential))
        assert first.status_code == 200
        assert first.json()["observation_document"] == serialize(item)

        grants.apply(record=GrantAdministrationRecord(
            "REVOKE-HTTP-READ", read_grant.principal,
            Action.REVOKE, read_grant, int(time.time()),
        ))
        second = client.get(ROUTE, headers=headers(credential))

    assert second.status_code == 403
    assert second.json() == {"status": "access_denied"}
    assert second.headers["cache-control"] == "no-store"
    assert item.description not in second.text
    assert setup.count(path) == 1


def test_another_signed_subject_has_no_implicit_access(tmp_path, keys):
    _, _, _, _, _, item, app = prepare(tmp_path, keys)
    credential = jwt_setup.token(
        keys[0], operations=(setup.READ,), overrides={"sub": "OTHER"},
    )
    with TestClient(app) as client:
        result = client.get(ROUTE, headers=headers(credential))
    assert result.status_code == 403
    assert result.json() == {"status": "access_denied"}
    assert item.description not in result.text
