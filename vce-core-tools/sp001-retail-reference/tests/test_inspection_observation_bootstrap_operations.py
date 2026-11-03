import sqlite3

import pytest
from fastapi.testclient import TestClient

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys  # pytest fixture
from test_inspection_observation_host_bootstrap import configuration
from test_inspection_observation_bootstrap_write_mode import (
    environment, write_headers, ROUTE as LEGACY_ROUTE,
)
import sp001.infrastructure.inspection_observation_host_bootstrap as bootstrap
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


ROUTE = "/v1/cases/CASE/inspection-observation-operations/REQUEST"


def operation_configuration(env, limit="1048576"):
    return {
        **env,
        bootstrap.PREFIX + "ACCESS_MODE": "READ_WRITE_OPERATIONS",
        bootstrap.PREFIX + "MAX_REQUEST_BYTES": limit,
    }


def tables(path):
    with sqlite3.connect(path) as connection:
        return {row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}


@pytest.mark.parametrize("mode", [None, "READ_ONLY", "READ_WRITE"])
def test_operations_require_explicit_new_mode(tmp_path, keys, mode):
    path, env = environment(tmp_path, keys)
    if mode is not None:
        env[bootstrap.PREFIX + "ACCESS_MODE"] = mode
    env[bootstrap.PREFIX + "MAX_REQUEST_BYTES"] = "1048576"
    app = bootstrap.create_app_from_environment(environment=env)
    with TestClient(app) as client:
        assert client.get(ROUTE).status_code == 404
        assert client.put(
            ROUTE,
            content=serialize(setup.observation(case_id="CASE")),
            headers=write_headers(keys),
        ).status_code == 404
    assert "retail_observation_operations" not in tables(path)


def test_explicit_operation_mode_saves_retries_and_recovers(tmp_path, keys):
    path, env = environment(tmp_path, keys)
    app = bootstrap.create_app_from_environment(
        environment=operation_configuration(env),
    )
    document = serialize(setup.observation(case_id="CASE"))
    with TestClient(app) as client:
        first = client.put(ROUTE, content=document, headers=write_headers(keys))
        assert first.status_code == 200
        assert first.json()["disposition"] == "CREATED"
        retry = client.put(ROUTE, content=document, headers=write_headers(keys))
        assert retry.status_code == 200
        assert retry.json() == first.json()
        read = {"Authorization": "Bearer " + jwt_setup.token(
            keys[0], operations=(setup.READ,),
        )}
        recovered = client.get(ROUTE, headers=read)
        assert recovered.status_code == 200
        assert recovered.json()["observation_document"] == document
    with sqlite3.connect(path) as connection:
        for table in (
            "retail_inspection_observations", "retail_observation_operations",
        ):
            assert connection.execute(
                "SELECT COUNT(*) FROM " + table
            ).fetchone()[0] == 1


def test_operation_mode_still_requires_current_save_permission(tmp_path, keys):
    path, env = environment(tmp_path, keys)
    app = bootstrap.create_app_from_environment(
        environment=operation_configuration(env),
    )
    with TestClient(app) as client:
        result = client.put(
            ROUTE, content=serialize(setup.observation(case_id="CASE")),
            headers={
                "Authorization": "Bearer " + jwt_setup.token(
                    keys[0], operations=(setup.READ,),
                ),
                "Content-Type": "application/json",
            },
        )
    assert result.status_code == 403
    assert setup.count(path) == 0


def test_operation_body_limit_is_effective(tmp_path, keys):
    path, env = environment(tmp_path, keys)
    app = bootstrap.create_app_from_environment(
        environment=operation_configuration(env, limit="10"),
    )
    with TestClient(app) as client:
        result = client.put(
            ROUTE, content=serialize(setup.observation(case_id="CASE")),
            headers=write_headers(keys),
        )
    assert result.status_code == 413
    assert setup.count(path) == 0


@pytest.mark.parametrize("value", [None, "", "0", "-1", "1.5", "１２"])
def test_invalid_operation_limit_precedes_schema_initialization(
    tmp_path, keys, value,
):
    path = tmp_path / "empty.sqlite3"
    path.touch()
    env = configuration(path, keys)
    env[bootstrap.PREFIX + "ACCESS_MODE"] = "READ_WRITE_OPERATIONS"
    if value is not None:
        env[bootstrap.PREFIX + "MAX_REQUEST_BYTES"] = value
    with pytest.raises(ValueError):
        bootstrap.create_app_from_environment(environment=env)
    assert tables(path) == set()


def test_legacy_write_remains_explicitly_receipt_free(tmp_path, keys):
    path, env = environment(tmp_path, keys)
    app = bootstrap.create_app_from_environment(
        environment=operation_configuration(env),
    )
    with TestClient(app) as client:
        result = client.put(
            LEGACY_ROUTE,
            content=serialize(setup.observation(case_id="CASE")),
            headers=write_headers(keys),
        )
    assert result.status_code == 200
    with sqlite3.connect(path) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM retail_observation_operations"
        ).fetchone()[0] == 0
