import pytest
from fastapi.testclient import TestClient

from test_case_state_http_host import Reader, state
from test_remote_case_state_reader import install_connection
from sp001.contracts.case_state_read_result import Found
from sp001.infrastructure.case_state_http_host import create_case_state_app
from sp001.infrastructure.remote_case_state_reader import RemoteCaseStateReader


def reader():
    return RemoteCaseStateReader(
        endpoint="https://coordinator.example/v1/cases/{caseId}/state",
        timeout_seconds=1, max_response_bytes=4096,
    )


@pytest.mark.parametrize("url", [
    "/v1/case-state?case_id=CASE-001",
    "/authoritative-state?case_id=CASE-001",
])
def test_retired_routes_are_infrastructure_404(url):
    source = Reader(Found(state()))
    with TestClient(create_case_state_app(
        reader=source, authorize=lambda request, case_id: True,
    )) as http:
        response = http.get(url)
    assert response.status_code == 404
    assert response.json().get("code") != "CASE_NOT_FOUND"
    assert source.calls == []


@pytest.mark.parametrize("case_id, target", [
    ("CASE-001", "/v1/cases/CASE-001/state"),
    ("CASE A", "/v1/cases/CASE%20A/state"),
    ("CASE?A#B", "/v1/cases/CASE%3FA%23B/state"),
    ("CASE%2FA", "/v1/cases/CASE%252FA/state"),
])
def test_client_encodes_identity_as_one_segment(monkeypatch, case_id, target):
    calls = install_connection(monkeypatch)
    reader().read(case_id=case_id)
    assert [call for call in calls if call[0] == "request"] == [
        ("request", "GET", target),
    ]


@pytest.mark.parametrize("case_id", [".", "..", "A/B", "A\\B", "A\nB", "A\x00B"])
def test_unsafe_segment_is_rejected_before_connection(monkeypatch, case_id):
    calls = install_connection(monkeypatch)
    with pytest.raises(ValueError):
        reader().read(case_id=case_id)
    assert calls == []


@pytest.mark.parametrize("case_id, encoded", [
    ("CASE A", "CASE%20A"),
    ("CASE?A#B", "CASE%3FA%23B"),
    ("CASE%2FA", "CASE%252FA"),
])
def test_host_preserves_encoded_identity(case_id, encoded):
    source = Reader(Found(state(case_id)))
    allowed = []
    app = create_case_state_app(
        reader=source,
        authorize=lambda request, identity: allowed.append(identity) or True,
    )
    status, payload = asgi_get(app, f"/v1/cases/{encoded}/state")
    assert status == 200
    assert payload["case_id"] == case_id
    assert allowed == [case_id]
    assert source.calls == [case_id]


def test_client_rejects_retired_endpoint_configuration():
    with pytest.raises(ValueError):
        RemoteCaseStateReader(
            endpoint="https://coordinator.example/v1/case-state",
            timeout_seconds=1, max_response_bytes=4096,
        )


def asgi_get(app, raw_target):
    import asyncio
    import json
    from urllib.parse import unquote

    async def run():
        messages = []
        received = False

        async def receive():
            nonlocal received
            if not received:
                received = True
                return {"type": "http.request", "body": b"", "more_body": False}
            await asyncio.Event().wait()

        async def send(message):
            messages.append(message)

        await app({
            "type": "http", "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1", "method": "GET", "scheme": "https",
            "path": unquote(raw_target, encoding="utf-8", errors="strict"),
            "raw_path": raw_target.encode("ascii"), "query_string": b"",
            "root_path": "", "headers": [],
            "server": ("localhost", 443), "client": ("127.0.0.1", 12345),
        }, receive, send)
        status = next(
            m["status"] for m in messages if m["type"] == "http.response.start"
        )
        body = b"".join(
            m.get("body", b"") for m in messages
            if m["type"] == "http.response.body"
        )
        return status, json.loads(body)

    return asyncio.run(run())


from test_case_state_https_loopback import https_host


@pytest.mark.parametrize("case_id", ["CASE A", "CASE?A#B", "CASE%2FA"])
def test_real_https_preserves_encoded_identity(https_host, case_id):
    from dataclasses import replace

    port, ca, source = https_host
    source.state = replace(source.state, case_id=case_id)
    remote = RemoteCaseStateReader(
        endpoint=f"https://localhost:{port}/v1/cases/{{caseId}}/state",
        timeout_seconds=2, max_response_bytes=4096, ca_file=str(ca),
    )
    result = remote.read(case_id=case_id)
    assert isinstance(result, Found)
    assert result.state.case_id == case_id
    assert source.calls == [case_id]
