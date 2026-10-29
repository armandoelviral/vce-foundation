import sqlite3

import pytest
from fastapi.testclient import TestClient

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys
from test_inspection_observation_host_bootstrap import configuration
import sp001.infrastructure.inspection_observation_host_bootstrap as bootstrap
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


ROUTE = "/v1/cases/CASE/inspection-observations/OBS-1/versions/1"


def environment(tmp_path, keys):
    path, _, _, _, _ = setup.environment(tmp_path, keys)
    return path, configuration(path, keys)


def write_configuration(env, limit="1048576"):
    return {
        **env,
        bootstrap.PREFIX + "ACCESS_MODE": "READ_WRITE",
        bootstrap.PREFIX + "MAX_REQUEST_BYTES": limit,
    }


def write_headers(keys):
    return {
        "Authorization": "Bearer " + jwt_setup.token(
            keys[0], operations=(setup.SAVE,),
        ),
        "Content-Type": "application/json",
    }


@pytest.mark.parametrize("explicit", [False, True])
def test_default_and_explicit_read_only_do_not_expose_put(tmp_path, keys, explicit):
    path, env = environment(tmp_path, keys)
    if explicit:
        env[bootstrap.PREFIX + "ACCESS_MODE"] = "READ_ONLY"
    app = bootstrap.create_app_from_environment(environment=env)
    with TestClient(app) as client:
        result = client.put(
            ROUTE, content=serialize(setup.observation(case_id="CASE")),
            headers=write_headers(keys),
        )
        assert client.get("/inspection-observations").status_code == 200
    assert result.status_code == 405
    assert setup.count(path) == 0


def test_explicit_read_write_saves_and_recovers(tmp_path, keys):
    path, env = environment(tmp_path, keys)
    app = bootstrap.create_app_from_environment(
        environment=write_configuration(env),
    )
    item = setup.observation(case_id="CASE")
    with TestClient(app) as client:
        for _ in range(2):
            result = client.put(
                ROUTE, content=serialize(item), headers=write_headers(keys),
            )
            assert result.status_code == 200
            assert result.json() == {
                "status": "saved", "observation_id": "OBS-1",
                "observation_version": "1",
            }
        recovered = client.get(ROUTE, headers={
            "Authorization": "Bearer " + jwt_setup.token(
                keys[0], operations=(setup.READ,),
            ),
        })
    assert recovered.status_code == 200
    assert recovered.json()["observation_document"] == serialize(item)
    assert setup.count(path) == 1


def test_write_mode_still_requires_save_permission(tmp_path, keys):
    path, env = environment(tmp_path, keys)
    app = bootstrap.create_app_from_environment(
        environment=write_configuration(env),
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


def test_configured_request_limit_is_effective(tmp_path, keys):
    path, env = environment(tmp_path, keys)
    app = bootstrap.create_app_from_environment(
        environment=write_configuration(env, limit="10"),
    )
    with TestClient(app) as client:
        result = client.put(
            ROUTE, content=serialize(setup.observation(case_id="CASE")),
            headers=write_headers(keys),
        )
    assert result.status_code == 413
    assert setup.count(path) == 0


@pytest.mark.parametrize("mode", ["", "read_write", "READ_WRITE ", "OTHER", None, True])
def test_invalid_mode_rejects_startup(tmp_path, keys, mode):
    _, env = environment(tmp_path, keys)
    env[bootstrap.PREFIX + "ACCESS_MODE"] = mode
    with pytest.raises(ValueError, match="access mode"):
        bootstrap.create_app_from_environment(environment=env)


@pytest.mark.parametrize("value", [None, "", "0", "-1", "1.5", "true", "１２"])
def test_write_mode_requires_valid_body_limit_before_schema_initialization(
    tmp_path, keys, value,
):
    path = tmp_path / "empty.sqlite3"
    path.touch()
    env = configuration(path, keys)
    env[bootstrap.PREFIX + "ACCESS_MODE"] = "READ_WRITE"
    if value is not None:
        env[bootstrap.PREFIX + "MAX_REQUEST_BYTES"] = value
    with pytest.raises(ValueError):
        bootstrap.create_app_from_environment(environment=env)

    with sqlite3.connect(path) as connection:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    assert tables == []


def test_body_limit_alone_does_not_enable_writes(tmp_path, keys):
    path, env = environment(tmp_path, keys)
    env[bootstrap.PREFIX + "MAX_REQUEST_BYTES"] = "1048576"
    app = bootstrap.create_app_from_environment(environment=env)
    with TestClient(app) as client:
        result = client.put(
            ROUTE, content=serialize(setup.observation(case_id="CASE")),
            headers=write_headers(keys),
        )
    assert result.status_code == 405
    assert setup.count(path) == 0
