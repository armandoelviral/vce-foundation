import sqlite3
from contextlib import closing
from pathlib import Path
import time
from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys  # pytest fixture
from test_authenticated_observation_operations_jwt import environment, request
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)
from sp001.infrastructure.observation_operation_http_host import (
    create_observation_operation_app,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


def arrange(tmp_path, keys):
    service, grants, definitions = environment(tmp_path, keys)
    client = TestClient(create_observation_operation_app(service=service))
    client.app.state.operation_database = Path(service._backend._path)
    item = request()
    route = (
        f"/v1/cases/{item.observation.case_id}/"
        f"inspection-observation-operations/{item.request_id}"
    )
    return client, grants, definitions, item, route


def headers(token):
    return {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    }


def token(keys, *operations, overrides=None, wrong_key=False):
    return jwt_setup.token(
        keys[1] if wrong_key else keys[0],
        operations=operations, overrides=overrides,
    )


def counts(client):
    path = client.app.state.operation_database.resolve()
    assert path.is_file(), "configured database must exist"
    uri = path.as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as connection:
        return tuple(connection.execute(
            "SELECT COUNT(*) FROM " + table
        ).fetchone()[0] for table in (
            "retail_inspection_observations",
            "retail_observation_operations",
        ))


def test_signed_save_retry_and_read_through_http(tmp_path, keys):
    client, _, _, item, route = arrange(tmp_path, keys)
    document = serialize(item.observation)
    write = headers(token(keys, setup.SAVE))
    read = headers(token(keys, setup.READ))

    first = client.put(route, content=document, headers=write)
    assert first.status_code == 200
    assert first.json()["status"] == "saved"
    assert first.json()["disposition"] == "CREATED"
    assert "observation_document" not in first.json()

    retry = client.put(route, content=document, headers=write)
    assert retry.status_code == 200
    assert retry.json() == first.json()

    recovered = client.get(route, headers=read)
    assert recovered.status_code == 200
    assert recovered.json()["status"] == "ok"
    assert recovered.json()["observation_document"] == document
    assert recovered.json()["disposition"] == "CREATED"
    assert recovered.headers["cache-control"] == "no-store"
    assert counts(client) == (1, 1)


@pytest.mark.parametrize("fault", ["signature", "expired", "audience"])
def test_invalid_signed_credential_leaves_no_pair(tmp_path, keys, fault):
    client, _, _, item, route = arrange(tmp_path, keys)
    overrides = {}
    if fault == "expired":
        now = int(time.time())
        overrides.update(iat=now-90, nbf=now-90, exp=now-1)
    elif fault == "audience":
        overrides["aud"] = "OTHER"
    credential = token(
        keys, setup.SAVE, setup.READ,
        overrides=overrides, wrong_key=fault == "signature",
    )
    result = client.put(
        route, content=serialize(item.observation), headers=headers(credential),
    )
    assert result.status_code == 401
    assert result.json()["status"] == "credential_rejected"
    assert "observation_document" not in result.json()
    assert counts(client) == (0, 0)


def test_read_and_write_permissions_remain_separate(tmp_path, keys):
    client, _, _, item, route = arrange(tmp_path, keys)
    denied_write = client.put(
        route, content=serialize(item.observation),
        headers=headers(token(keys, setup.READ)),
    )
    assert denied_write.status_code == 403
    denied_read = client.get(
        route, headers=headers(token(keys, setup.SAVE)),
    )
    assert denied_read.status_code == 403
    assert counts(client) == (0, 0)


def test_absence_is_authorized_and_case_scoped(tmp_path, keys):
    client, _, _, item, route = arrange(tmp_path, keys)
    credential = headers(token(keys, setup.READ))
    missing = client.get(route, headers=credential)
    assert missing.status_code == 404
    assert missing.json() == {"status": "operation_not_found"}

    other_route = route.replace(
        "/cases/" + item.observation.case_id + "/",
        "/cases/OTHER/",
    )
    denied = client.get(other_route, headers=credential)
    assert denied.status_code == 403
    assert "observation_document" not in denied.json()


def test_revocation_blocks_same_token_without_erasing_pair(tmp_path, keys):
    client, grants, definitions, item, route = arrange(tmp_path, keys)
    credential = headers(token(keys, setup.SAVE, setup.READ))
    document = serialize(item.observation)
    assert client.put(
        route, content=document, headers=credential,
    ).status_code == 200
    assert client.get(route, headers=credential).status_code == 200

    for index, grant in enumerate(definitions):
        assert grants.apply(record=GrantAdministrationRecord(
            f"HTTP-OP-REVOKE-{index}",
            grant.principal, Action.REVOKE, grant, int(time.time()),
        ))

    retry = client.put(route, content=document, headers=credential)
    recovered = client.get(route, headers=credential)
    assert retry.status_code == 403
    assert recovered.status_code == 403
    assert "observation_document" not in retry.json()
    assert "observation_document" not in recovered.json()
    assert counts(client) == (1, 1)


def test_conflicting_http_retry_preserves_original(tmp_path, keys):
    client, _, _, item, route = arrange(tmp_path, keys)
    credential = headers(token(keys, setup.SAVE, setup.READ))
    original = serialize(item.observation)
    assert client.put(
        route, content=original, headers=credential,
    ).status_code == 200

    changed = serialize(replace(
        item.observation, description="Contradictory HTTP request.",
    ))
    conflict = client.put(route, content=changed, headers=credential)
    assert conflict.status_code == 409
    assert conflict.json()["status"] == "operation_conflict"

    recovered = client.get(route, headers=credential)
    assert recovered.status_code == 200
    assert recovered.json()["observation_document"] == original
    assert counts(client) == (1, 1)
