import pytest
from fastapi.testclient import TestClient

import test_retail_report_attribution_admission as setup

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction,
    GrantAdministrationRecord,
)
from sp001.infrastructure.retail_report_read_http_host import (
    create_retail_report_read_app,
)


ROUTE = "/v1/cases/CASE/retail-reports/REPORT"


def test_authorized_synthetic_report_is_returned(tmp_path):
    _, _, _, report, _, _, _, _, _, _, service = setup.environment(tmp_path)
    setup.save(service, report)

    client = TestClient(create_retail_report_read_app(service=service))
    result = client.get(ROUTE, headers={"Authorization": "Bearer valid"})

    assert result.status_code == 200
    assert result.json()["status"] == "ok"
    assert isinstance(result.json()["report_text"], str)
    assert result.json()["report_text"]
    assert result.headers["cache-control"] == "no-store"


@pytest.mark.parametrize("header", [None, "Bearer invalid", "Basic invalid"])
def test_rejected_credential_returns_no_report(tmp_path, header):
    _, _, _, report, _, _, _, _, _, _, service = setup.environment(tmp_path)
    setup.save(service, report)

    client = TestClient(create_retail_report_read_app(service=service))
    headers = {} if header is None else {"Authorization": header}
    result = client.get(ROUTE, headers=headers)

    assert result.status_code == 401
    assert result.json() == {"status": "credential_rejected"}
    assert result.headers["cache-control"] == "no-store"


def test_revoked_grants_are_denied_without_report_content(tmp_path):
    (
        _, _, principal, report, _, _, grants, definitions,
        _, _, service,
    ) = setup.environment(tmp_path)
    setup.save(service, report)

    for index, grant in enumerate(definitions):
        grants.apply(record=GrantAdministrationRecord(
            f"HTTP-REVOKE-{index}",
            principal,
            GrantAdministrationAction.REVOKE,
            grant,
            150,
        ))

    client = TestClient(create_retail_report_read_app(service=service))
    result = client.get(ROUTE, headers={"Authorization": "Bearer valid"})

    assert result.status_code == 403
    assert result.json() == {"status": "access_denied"}
    assert result.headers["cache-control"] == "no-store"


def test_authorized_absence_is_distinct(tmp_path):
    _, _, _, _, _, _, _, _, _, _, service = setup.environment(tmp_path)

    client = TestClient(create_retail_report_read_app(service=service))
    result = client.get(
        "/v1/cases/CASE/retail-reports/MISSING",
        headers={"Authorization": "Bearer valid"},
    )

    assert result.status_code == 404
    assert result.json() == {"status": "report_not_found"}
    assert result.headers["cache-control"] == "no-store"


def test_backend_failure_is_not_report_absence():
    class BrokenService:
        def recover_with_admissions(self, **kwargs):
            raise OSError("synthetic backend failure")

    client = TestClient(create_retail_report_read_app(service=BrokenService()))
    result = client.get(ROUTE, headers={"Authorization": "Bearer valid"})

    assert result.status_code == 503
    assert result.json() == {"status": "backend_unavailable"}
    assert result.headers["cache-control"] == "no-store"
\


def test_expiration_during_render_returns_no_report(tmp_path, monkeypatch):
    import sp001.infrastructure.retail_report_read_http_host as host

    _, now, _, report, _, _, _, _, _, _, service = setup.environment(tmp_path)
    setup.save(service, report)

    original_render = host.render_retail_vm_report_text

    def render_then_expire(**kwargs):
        rendered = original_render(**kwargs)
        now[0] = 300  # El contexto del fixture expira en 300.
        return rendered

    monkeypatch.setattr(host, "render_retail_vm_report_text", render_then_expire)

    client = TestClient(create_retail_report_read_app(service=service))
    result = client.get(ROUTE, headers={"Authorization": "Bearer valid"})

    assert result.status_code == 401
    assert result.json() == {"status": "credential_rejected"}
    assert result.headers["cache-control"] == "no-store"


def test_revocation_during_render_returns_no_report(tmp_path, monkeypatch):
    import sp001.infrastructure.retail_report_read_http_host as host

    (
        _, _, principal, report, _, _, grants, definitions,
        _, _, service,
    ) = setup.environment(tmp_path)
    setup.save(service, report)

    original_render = host.render_retail_vm_report_text

    def render_then_revoke(**kwargs):
        rendered = original_render(**kwargs)
        for index, grant in enumerate(definitions):
            grants.apply(record=GrantAdministrationRecord(
                f"HTTP-RENDER-REVOKE-{index}",
                principal,
                GrantAdministrationAction.REVOKE,
                grant,
                150,
            ))
        return rendered

    monkeypatch.setattr(host, "render_retail_vm_report_text", render_then_revoke)

    client = TestClient(create_retail_report_read_app(service=service))
    result = client.get(ROUTE, headers={"Authorization": "Bearer valid"})

    assert result.status_code == 403
    assert result.json() == {"status": "access_denied"}
    assert result.headers["cache-control"] == "no-store"
