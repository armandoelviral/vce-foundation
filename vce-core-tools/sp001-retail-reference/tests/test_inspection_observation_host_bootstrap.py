import pytest
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from fastapi.testclient import TestClient

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys
import sp001.infrastructure.inspection_observation_host_bootstrap as bootstrap
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


ROUTE = "/v1/cases/CASE/inspection-observations/OBS-1/versions/1"


def configuration(path, keys):
    values = {
        "DATABASE": str(path),
        "ISSUER": jwt_setup.ISSUER,
        "AUDIENCE": jwt_setup.AUDIENCE,
        "KEY_ID": "KEY-1",
        "PUBLIC_KEY_PEM": keys[0].public_key().public_bytes(
            Encoding.PEM, PublicFormat.SubjectPublicKeyInfo,
        ).decode("ascii"),
        "MAX_LIFETIME_SECONDS": "120",
        "MAX_TOKEN_BYTES": "16384",
    }
    return {bootstrap.PREFIX + name: value for name, value in values.items()}


def test_bootstrap_recovers_existing_observation(tmp_path, keys):
    path, service, _, _, _ = setup.environment(tmp_path, keys)
    item = setup.observation(case_id=setup.CASE)
    service.save(
        credential=jwt_setup.token(keys[0], operations=(setup.SAVE,)),
        observation=item,
    )
    app = bootstrap.create_app_from_environment(
        environment=configuration(path, keys),
    )
    credential = jwt_setup.token(keys[0], operations=(setup.READ,))
    with TestClient(app) as client:
        result = client.get(
            ROUTE, headers={"Authorization": f"Bearer {credential}"},
        )
    assert result.status_code == 200
    assert result.json() == {
        "status": "ok", "observation_document": serialize(item),
    }
    assert result.headers["cache-control"] == "no-store"
    assert setup.count(path) == 1


@pytest.mark.parametrize("name", [
    "DATABASE", "ISSUER", "AUDIENCE", "KEY_ID", "PUBLIC_KEY_PEM",
    "MAX_LIFETIME_SECONDS", "MAX_TOKEN_BYTES",
])
def test_missing_configuration_rejects_startup(tmp_path, keys, name):
    path = tmp_path / "existing.sqlite3"
    path.touch()
    env = configuration(path, keys)
    del env[bootstrap.PREFIX + name]
    with pytest.raises(ValueError, match="missing configuration"):
        bootstrap.create_app_from_environment(environment=env)


@pytest.mark.parametrize("name", ["MAX_LIFETIME_SECONDS", "MAX_TOKEN_BYTES"])
@pytest.mark.parametrize("value", ["0", "-1", "1.5", "true", "１２", " 120"])
def test_invalid_limit_rejects_startup(tmp_path, keys, name, value):
    path = tmp_path / "existing.sqlite3"
    path.touch()
    env = configuration(path, keys)
    env[bootstrap.PREFIX + name] = value
    with pytest.raises(ValueError):
        bootstrap.create_app_from_environment(environment=env)


def test_missing_database_is_not_created(tmp_path, keys):
    path = tmp_path / "missing.sqlite3"
    with pytest.raises(ValueError, match="already exist"):
        bootstrap.create_app_from_environment(
            environment=configuration(path, keys),
        )
    assert not path.exists()


def test_directory_is_not_a_database_file(tmp_path, keys):
    with pytest.raises(ValueError, match="already exist"):
        bootstrap.create_app_from_environment(
            environment=configuration(tmp_path, keys),
        )


@pytest.mark.parametrize("pem", ["PRIVATE-TEST-KEY-MARKER", "not-a-key-ñ"])
def test_invalid_key_rejects_startup_without_echoing_value(tmp_path, keys, pem):
    path = tmp_path / "existing.sqlite3"
    path.touch()
    env = configuration(path, keys)
    env[bootstrap.PREFIX + "PUBLIC_KEY_PEM"] = pem
    with pytest.raises(ValueError, match="verification key") as caught:
        bootstrap.create_app_from_environment(environment=env)
    assert str(caught.value) == "invalid public verification key"
    assert pem not in str(caught.value)


def test_factory_uses_process_environment(monkeypatch):
    sentinel = object()
    supplied = {}

    def compose(*, environment):
        supplied["environment"] = environment
        return sentinel

    monkeypatch.setattr(bootstrap, "create_app_from_environment", compose)
    assert bootstrap.create_app() is sentinel
    assert supplied["environment"] is bootstrap.os.environ


def test_report_configuration_does_not_implicitly_configure_observations(
    tmp_path, keys,
):
    path = tmp_path / "existing.sqlite3"
    path.touch()
    env = {
        name.replace(bootstrap.PREFIX, "SP001_RETAIL_REPORT_", 1): value
        for name, value in configuration(path, keys).items()
    }
    with pytest.raises(ValueError, match="missing configuration"):
        bootstrap.create_app_from_environment(environment=env)
