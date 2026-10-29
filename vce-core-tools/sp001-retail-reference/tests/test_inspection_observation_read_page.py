import pytest
from fastapi.testclient import TestClient

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys

from sp001.infrastructure.inspection_observation_read_http_host import (
    create_inspection_observation_read_app,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


class MustNotRead:
    def recover(self, **kwargs):
        raise AssertionError("public page must not query observation storage")


def test_public_shell_does_not_read_observations():
    with TestClient(create_inspection_observation_read_app(
        service=MustNotRead(),
    )) as client:
        result = client.get("/inspection-observations")
    assert result.status_code == 200
    for field in ("case", "observation", "version", "credential", "query"):
        assert f'id="{field}"' in result.text
    assert 'id="output" hidden' in result.text
    assert 'type="password"' in result.text
    assert "responsable del documento es declarado" in result.text
    assert result.headers["cache-control"] == "no-store"
    assert "connect-src 'self'" in result.headers["content-security-policy"]
    assert "frame-ancestors 'none'" in result.headers["content-security-policy"]


@pytest.mark.parametrize("asset,mime", [
    ("read.js", "text/javascript"),
    ("read.css", "text/css"),
])
def test_assets_are_served_with_security_headers(asset, mime):
    with TestClient(create_inspection_observation_read_app(
        service=MustNotRead(),
    )) as client:
        result = client.get("/inspection-observations/assets/" + asset)
    assert result.status_code == 200
    assert result.headers["content-type"].startswith(mime)
    assert result.headers["cache-control"] == "no-store"
    assert result.headers["x-content-type-options"] == "nosniff"
    assert result.headers["referrer-policy"] == "no-referrer"


def test_same_host_retains_jwt_authorized_endpoint(tmp_path, keys):
    _, service, _, _, _ = setup.environment(tmp_path, keys)
    item = setup.observation(case_id=setup.CASE)
    service.save(
        credential=jwt_setup.token(keys[0], operations=(setup.SAVE,)),
        observation=item,
    )
    route = "/v1/cases/CASE/inspection-observations/OBS-1/versions/1"
    with TestClient(create_inspection_observation_read_app(
        service=service,
    )) as client:
        assert client.get("/inspection-observations").status_code == 200
        rejected = client.get(route)
        assert rejected.status_code == 401
        assert rejected.json() == {"status": "credential_rejected"}
        accepted = client.get(route, headers={
            "Authorization": "Bearer " + jwt_setup.token(
                keys[0], operations=(setup.READ,),
            ),
        })
    assert accepted.status_code == 200
    assert accepted.json() == {
        "status": "ok", "observation_document": serialize(item),
    }
