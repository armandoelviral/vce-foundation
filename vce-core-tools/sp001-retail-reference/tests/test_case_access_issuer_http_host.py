from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from test_federated_case_access_issuance_integration import flow
from sp001.contracts.case_access_issuance_policy import CaseAccessIssuancePolicy
from sp001.contracts.case_access_grant_administration import GrantAdministrationAction
from sp001.infrastructure.case_access_issuer_http_host import create_case_access_issuer_app

URL = "/v1/case-access-token"
BODY = {"request_id": "HTTP-REQUEST", "case_id": "CASE-001", "operation": "READ_STATE"}


@pytest.fixture
def host(flow, monkeypatch):
    store, service, _, command, primary, _ = flow
    monkeypatch.setattr(service, "_issuance_policy", CaseAccessIssuancePolicy(
        "issuance-service", "access", "coordinator", "KEY-1", 120,
    ))
    app = create_case_access_issuer_app(
        service=service, max_request_bytes=1024, max_primary_credential_bytes=8192,
    )
    with TestClient(app) as client:
        yield client, store, service, command, primary


def test_http_issues_only_after_completion_and_replays_exact_token(host):
    client, store, _, _, primary = host
    headers = {"Authorization": "Bearer " + primary()}
    response = client.post(URL, headers=headers, json=BODY)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert store.read_completed(request_id=BODY["request_id"]) is not None
    assert response.headers["cache-control"] == "no-store"
    replay = client.post(URL, headers=headers, json=BODY)
    assert replay.status_code == 200
    assert replay.json()["access_token"] == token


def test_missing_authentication_does_not_prepare(host):
    client, store, _, _, _ = host
    response = client.post(URL, json=BODY)
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert store.read_prepared(request_id=BODY["request_id"]) is None


@pytest.mark.parametrize("change", [
    {"subject": "chosen"}, {"audience": "chosen"}, {"expires_at": 9999999999},
])
def test_client_cannot_supply_security_fields(host, change):
    client, store, _, _, primary = host
    response = client.post(
        URL, headers={"Authorization": "Bearer " + primary()}, json={**BODY, **change},
    )
    assert response.status_code == 400
    assert store.read_prepared(request_id=BODY["request_id"]) is None


def test_same_identifier_with_different_case_is_conflict(host):
    client, _, _, _, primary = host
    headers = {"Authorization": "Bearer " + primary()}
    assert client.post(URL, headers=headers, json=BODY).status_code == 200
    response = client.post(URL, headers=headers, json={**BODY, "case_id": "OTHER"})
    assert response.status_code == 409


def test_revocation_denies_recovery_without_returning_token(host):
    client, store, _, command, primary = host
    headers = {"Authorization": "Bearer " + primary()}
    assert client.post(URL, headers=headers, json=BODY).status_code == 200
    store.apply(record=replace(
        command, event_id="HTTP-REVOKE", action=GrantAdministrationAction.REVOKE,
    ))
    response = client.post(URL, headers=headers, json=BODY)
    assert response.status_code == 403
    assert "access_token" not in response.json()


def test_provider_failure_returns_503_without_preparation(host, monkeypatch):
    client, store, service, _, primary = host

    def unavailable(**kwargs):
        from sp001.infrastructure.jwt_case_access_authenticator import AccessTokenKeyResolutionError
        raise AccessTokenKeyResolutionError("sensitive provider details")

    monkeypatch.setattr(service._authenticator, "authenticate", unavailable)
    response = client.post(
        URL, headers={"Authorization": "Bearer " + primary()}, json=BODY,
    )
    assert response.status_code == 503
    assert "sensitive" not in response.text
    assert store.read_prepared(request_id=BODY["request_id"]) is None


def test_duplicate_json_and_large_body_are_rejected(host):
    client, store, _, _, primary = host
    headers = {
        "Authorization": "Bearer " + primary(), "Content-Type": "application/json",
    }
    duplicate = (
        '{"request_id":"HTTP-REQUEST","request_id":"OTHER",'
        '"case_id":"CASE-001","operation":"READ_STATE"}'
    )
    assert client.post(URL, headers=headers, content=duplicate).status_code == 400
    assert client.post(URL, headers=headers, content="x" * 1025).status_code == 413
    assert store.read_prepared(request_id=BODY["request_id"]) is None
