from pathlib import Path

import pytest
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)
from fastapi.testclient import TestClient

import test_retail_report_jwt_composition as setup
from test_retail_report_jwt_composition import keys  # pytest fixture

import sp001.infrastructure.retail_report_host_bootstrap as bootstrap


def configuration(path, keys):
    return {
        "SP001_RETAIL_REPORT_DATABASE": str(path),
        "SP001_RETAIL_REPORT_ISSUER": setup.ISSUER,
        "SP001_RETAIL_REPORT_AUDIENCE": setup.AUDIENCE,
        "SP001_RETAIL_REPORT_KEY_ID": "KEY-1",
        "SP001_RETAIL_REPORT_PUBLIC_KEY_PEM": keys[0].public_key().public_bytes(
            Encoding.PEM,
            PublicFormat.SubjectPublicKeyInfo,
        ).decode("ascii"),
        "SP001_RETAIL_REPORT_MAX_LIFETIME_SECONDS": "120",
        "SP001_RETAIL_REPORT_MAX_TOKEN_BYTES": "16384",
    }


def test_bootstrap_recovers_existing_report(tmp_path, keys):
    path, service, _, _ = setup.environment(tmp_path, keys)
    report = setup.make_report()
    service.save(
        credential=setup.token(keys[0]),
        identity=setup.IDENTITY,
        report=report,
    )

    app = bootstrap.create_app_from_environment(
        environment=configuration(path, keys),
    )
    client = TestClient(app)
    result = client.get(
        "/v1/cases/CASE/retail-reports/REPORT-1",
        headers={"Authorization": f"Bearer {setup.token(keys[0])}"},
    )

    assert result.status_code == 200
    assert result.json()["status"] == "ok"
    assert result.json()["report_text"]
    assert setup.row_count(path) == 1


@pytest.mark.parametrize("name", [
    "DATABASE",
    "ISSUER",
    "AUDIENCE",
    "KEY_ID",
    "PUBLIC_KEY_PEM",
    "MAX_LIFETIME_SECONDS",
    "MAX_TOKEN_BYTES",
])
def test_missing_configuration_rejects_startup(tmp_path, keys, name):
    path, _, _, _ = setup.environment(tmp_path, keys)
    env = configuration(path, keys)
    del env["SP001_RETAIL_REPORT_" + name]

    with pytest.raises(ValueError):
        bootstrap.create_app_from_environment(environment=env)


@pytest.mark.parametrize("value", ["0", "-1", "1.5", "true"])
def test_invalid_limit_rejects_startup(tmp_path, keys, value):
    path, _, _, _ = setup.environment(tmp_path, keys)
    env = configuration(path, keys)
    env["SP001_RETAIL_REPORT_MAX_TOKEN_BYTES"] = value

    with pytest.raises(ValueError):
        bootstrap.create_app_from_environment(environment=env)


def test_missing_database_is_not_created(tmp_path, keys):
    path = tmp_path / "missing.sqlite3"
    env = configuration(path, keys)

    with pytest.raises(ValueError, match="already exist"):
        bootstrap.create_app_from_environment(environment=env)

    assert not path.exists()


def test_invalid_key_rejects_startup(tmp_path, keys):
    path, _, _, _ = setup.environment(tmp_path, keys)
    env = configuration(path, keys)
    env["SP001_RETAIL_REPORT_PUBLIC_KEY_PEM"] = "invalid"

    with pytest.raises(ValueError, match="verification key"):
        bootstrap.create_app_from_environment(environment=env)


def test_uvicorn_factory_uses_environment(monkeypatch):
    sentinel = object()
    supplied = {}

    def compose(*, environment):
        supplied["environment"] = environment
        return sentinel

    monkeypatch.setattr(bootstrap, "create_app_from_environment", compose)

    assert bootstrap.create_app() is sentinel
    assert supplied["environment"] is bootstrap.os.environ
