import pytest
from fastapi.testclient import TestClient

from sp001.infrastructure.inspection_observation_read_http_host import (
    create_inspection_observation_read_app,
)
from sp001.infrastructure.inspection_observation_http_host import (
    create_inspection_observation_app,
)


class MustNotAccess:
    def recover(self, **kwargs):
        raise AssertionError("loading the form must not read storage")

    def save(self, **kwargs):
        raise AssertionError("loading the form must not write storage")


def test_capture_shell_preserves_declared_scope_without_storage_access():
    with TestClient(create_inspection_observation_app(
        service=MustNotAccess(),
    )) as client:
        result = client.get("/inspection-observations/capture")
    assert result.status_code == 200
    for field in (
        "case_id", "observation_id", "observation_version",
        "subject_reference", "description", "scope", "limitations",
        "evidence_ids", "actor_id", "customer_id", "organization_id",
        "role_id", "role_name", "actor_type", "method",
        "observed_at", "recorded_at", "credential",
    ):
        assert f'id="{field}"' in result.text
    assert "sin dictamen" in result.text.lower()
    assert "no acredita autoría" in result.text
    assert result.headers["cache-control"] == "no-store"
    assert "form-action 'none'" in result.headers["content-security-policy"]


@pytest.mark.parametrize("asset,mime", [
    ("form.js", "text/javascript"), ("form.css", "text/css"),
])
def test_capture_assets_are_same_origin_and_no_store(asset, mime):
    with TestClient(create_inspection_observation_app(
        service=MustNotAccess(),
    )) as client:
        result = client.get(
            "/inspection-observations/capture/assets/" + asset,
        )
    assert result.status_code == 200
    assert result.headers["content-type"].startswith(mime)
    assert result.headers["cache-control"] == "no-store"
    assert result.headers["x-content-type-options"] == "nosniff"


@pytest.mark.parametrize("route", [
    "/inspection-observations/capture",
    "/inspection-observations/capture/assets/form.js",
    "/inspection-observations/capture/assets/form.css",
])
def test_read_only_factory_does_not_expose_capture(route):
    with TestClient(create_inspection_observation_read_app(
        service=MustNotAccess(),
    )) as client:
        assert client.get(route).status_code == 404
