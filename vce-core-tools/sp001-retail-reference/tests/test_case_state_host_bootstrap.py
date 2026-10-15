import json

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from fastapi.testclient import TestClient

from sp001.infrastructure.case_state_host_bootstrap import create_app_from_environment
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants


@pytest.fixture
def environment(tmp_path):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    path = tmp_path / "public-keys.json"
    path.write_text(json.dumps({"key-1": pem}))
    return {
        "SP001_AUTH_ISSUER": "https://issuer.example",
        "SP001_AUTH_AUDIENCE": "sp001-coordinator",
        "SP001_AUTH_PUBLIC_KEYS_FILE": str(path),
        "SP001_AUTH_MAX_LIFETIME_SECONDS": "300",
        "SP001_AUTH_MAX_TOKEN_BYTES": "8192",
        "SP001_CASE_DATABASE_PATH": str(tmp_path / "cases.sqlite3"),
        "SP001_GRANTS_DATABASE_PATH": str(tmp_path / "grants.sqlite3"),
    }


def assert_no_databases(environment):
    from pathlib import Path
    assert not Path(environment["SP001_CASE_DATABASE_PATH"]).exists()
    assert not Path(environment["SP001_GRANTS_DATABASE_PATH"]).exists()


@pytest.mark.parametrize("name", [
    "SP001_AUTH_ISSUER", "SP001_AUTH_AUDIENCE",
    "SP001_AUTH_PUBLIC_KEYS_FILE", "SP001_AUTH_MAX_LIFETIME_SECONDS",
    "SP001_AUTH_MAX_TOKEN_BYTES", "SP001_CASE_DATABASE_PATH",
    "SP001_GRANTS_DATABASE_PATH",
])
def test_missing_configuration_creates_no_database(environment, name):
    invalid = dict(environment)
    del invalid[name]
    with pytest.raises(ValueError):
        create_app_from_environment(environment=invalid)
    assert_no_databases(environment)


@pytest.mark.parametrize("value", ["0", "-1", "1.5", "true", " 300"])
def test_invalid_limit_creates_no_database(environment, value):
    invalid = dict(environment)
    invalid["SP001_AUTH_MAX_LIFETIME_SECONDS"] = value
    with pytest.raises(ValueError):
        create_app_from_environment(environment=invalid)
    assert_no_databases(environment)


def test_invalid_key_creates_no_database(environment):
    from pathlib import Path
    Path(environment["SP001_AUTH_PUBLIC_KEYS_FILE"]).write_text(
        '{"key-1":"invalid PEM"}'
    )
    with pytest.raises(ValueError):
        create_app_from_environment(environment=environment)
    assert_no_databases(environment)


def test_same_database_paths_are_rejected(environment):
    invalid = dict(environment)
    invalid["SP001_GRANTS_DATABASE_PATH"] = invalid["SP001_CASE_DATABASE_PATH"]
    with pytest.raises(ValueError):
        create_app_from_environment(environment=invalid)
    assert_no_databases(environment)


def test_relative_database_path_is_rejected_before_creation(environment):
    invalid = dict(environment)
    invalid["SP001_GRANTS_DATABASE_PATH"] = "relative-grants.sqlite3"
    with pytest.raises(ValueError):
        create_app_from_environment(environment=invalid)
    assert_no_databases(environment)


def test_valid_configuration_builds_authenticated_host_without_default_grants(environment):
    app = create_app_from_environment(environment=environment)
    with TestClient(app) as client:
        response = client.get("/v1/cases/CASE-001/state")
    assert response.status_code == 401
    assert SqliteCaseAccessGrants(
        database_path=environment["SP001_GRANTS_DATABASE_PATH"]
    ).read_audit() == ()
