from fastapi.testclient import TestClient

import test_retail_report_jwt_composition as setup
from test_retail_report_jwt_composition import keys  # pytest fixture

from sp001.infrastructure.retail_report_read_http_host import (
    create_retail_report_read_app,
)


def test_public_page_contains_no_report_or_credential(tmp_path, keys):
    _, _, _, _ = setup.environment(tmp_path, keys)

    class MustNotRead:
        def recover_with_admissions(self, **kwargs):
            raise AssertionError("loading the page must not read a report")

    client = TestClient(create_retail_report_read_app(service=MustNotRead()))
    response = client.get("/retail-reports")

    assert response.status_code == 200
    assert 'id="query"' in response.text
    assert 'id="output" hidden' in response.text
    assert "Synthetic rationale." not in response.text
    assert response.headers["cache-control"] == "no-store"
    assert "connect-src 'self'" in response.headers["content-security-policy"]


def test_page_assets_are_served_from_same_host(tmp_path, keys):
    _, service, _, _ = setup.environment(tmp_path, keys)
    client = TestClient(create_retail_report_read_app(service=service))

    for resource in ("read.js", "read.css"):
        response = client.get("/retail-reports/assets/" + resource)
        assert response.status_code == 200
        assert response.headers["cache-control"] == "no-store"
        assert response.headers["x-content-type-options"] == "nosniff"


def test_same_host_retains_authorized_report_endpoint(tmp_path, keys):
    _, service, _, _ = setup.environment(tmp_path, keys)
    service.save(
        credential=setup.token(keys[0]),
        identity=setup.IDENTITY,
        report=setup.make_report(),
    )
    client = TestClient(create_retail_report_read_app(service=service))

    assert client.get("/retail-reports").status_code == 200

    route = "/v1/cases/CASE/retail-reports/REPORT-1"
    denied = client.get(route)
    assert denied.status_code == 401
    assert denied.json() == {"status": "credential_rejected"}

    accepted = client.get(
        route,
        headers={"Authorization": f"Bearer {setup.token(keys[0])}"},
    )
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "ok"
    assert accepted.json()["report_text"]
