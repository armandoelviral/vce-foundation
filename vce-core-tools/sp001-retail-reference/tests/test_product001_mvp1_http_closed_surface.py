"""F.4C.2A.1: protected laboratory HTTP surface remains closed."""

from fastapi.testclient import TestClient
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)

from sp001.infrastructure.product001_mvp1_http_host import (
    create_product001_mvp1_http_app,
)
from sp001.infrastructure.product001_mvp1_protected_composition import (
    compose_product001_mvp1_protected_approval,
)

from test_product001_commercial_approval_composed_integration import (
    environment,
)


def test_protected_host_exposes_no_commercial_write_route(environment):
    authority = Ed25519PrivateKey.generate()
    protected = compose_product001_mvp1_protected_approval(
        authenticated_service=environment["service"],
        authority_public_key=authority.public_key(),
    )

    app = create_product001_mvp1_http_app(
        protected_service=protected,
    )

    with TestClient(app) as client:
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            response = client.request(
                method,
                "/laboratory/product001/mvp1/decisions",
                json={},
            )
            assert response.status_code == 404

        for path in (
            "/openapi.json",
            "/docs",
            "/redoc",
        ):
            assert client.get(path).status_code == 404


def test_protected_host_has_no_business_routes(environment):
    authority = Ed25519PrivateKey.generate()
    protected = compose_product001_mvp1_protected_approval(
        authenticated_service=environment["service"],
        authority_public_key=authority.public_key(),
    )

    app = create_product001_mvp1_http_app(
        protected_service=protected,
    )

    assert not any(
        route.path.startswith("/laboratory/product001")
        for route in app.routes
    )
