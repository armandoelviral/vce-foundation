import ast
from pathlib import Path

import pytest

from test_case_access_issuance_completion import components
from test_authenticated_case_access_issuance import Authenticator
from sp001.contracts.case_access_issuance_backend import CaseAccessIssuanceBackend
from sp001.contracts.case_access_token_issuance import IssuedCaseAccessToken
from sp001.services.authenticated_case_access_issuance import (
    AuthenticatedCaseAccessIssuance, IssuanceAuthenticationRejected,
    IssuanceIdentityRejected,
)


class Backend:
    """Control-flow double; makes no durability claim."""

    def __init__(self, preparation):
        self.preparation = preparation
        self.calls = []

    def prepare(self, *, preparation, at_time, before_commit=None):
        self.calls.append("prepare")
        if before_commit is not None:
            before_commit()
        return preparation

    def prepare_request(self, *, request, context, policy, clock):
        self.calls.append("prepare_request")
        return self.preparation

    def read_prepared(self, *, request_id):
        self.calls.append("read")
        return self.preparation

    def complete(self, *, request_id, before_commit=None):
        self.calls.append("complete")
        if before_commit is not None:
            before_commit()
        return IssuedCaseAccessToken("opaque-credential")


def service(backend, principal, clock=lambda: 150):
    return AuthenticatedCaseAccessIssuance(
        authenticator=Authenticator(principal),
        backend=backend, expected_audience="issuance-service", clock=clock,
    )


def test_application_accepts_non_sqlite_backend(components):
    preparation = components[4]
    backend = Backend(preparation)
    assert isinstance(backend, CaseAccessIssuanceBackend)
    boundary = service(backend, preparation.binding.external_principal)
    assert boundary.prepare(
        credential="primary", preparation=preparation,
    ) == preparation
    assert boundary.complete(
        credential="primary", request_id=preparation.request_id,
    ).credential == "opaque-credential"
    assert backend.calls == ["prepare", "read", "complete"]


def test_rejected_authentication_never_reaches_backend(components):
    backend = Backend(components[4])
    boundary = service(backend, None)
    with pytest.raises(IssuanceAuthenticationRejected):
        boundary.complete(credential="invalid", request_id="REQUEST-1")
    assert backend.calls == []


def test_foreign_identity_never_reaches_completion(components):
    from dataclasses import replace
    preparation = components[4]
    backend = Backend(preparation)
    foreign = replace(preparation.binding.external_principal, subject="OTHER")
    boundary = service(backend, foreign)
    with pytest.raises(IssuanceIdentityRejected):
        boundary.complete(
            credential="foreign", request_id=preparation.request_id,
        )
    assert backend.calls == ["read"]


def test_expiry_after_backend_completion_prevents_delivery(components):
    preparation = components[4]
    now = [150]

    class ExpiringBackend(Backend):
        def complete(self, *, request_id, before_commit=None):
            token = super().complete(
                request_id=request_id, before_commit=before_commit,
            )
            now[0] = 200
            return token

    backend = ExpiringBackend(preparation)
    boundary = service(
        backend, preparation.binding.external_principal, clock=lambda: now[0],
    )
    with pytest.raises(IssuanceAuthenticationRejected):
        boundary.complete(
            credential="primary", request_id=preparation.request_id,
        )
    assert backend.calls == ["read", "complete"]


def test_incomplete_backend_is_rejected():
    with pytest.raises(TypeError, match="backend"):
        service(object(), None)


def test_application_has_no_infrastructure_import_or_private_store_access():
    path = Path("src/sp001/services/authenticated_case_access_issuance.py")
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert not (node.module or "").startswith("sp001.infrastructure")
        if isinstance(node, ast.Import):
            assert not any(
                alias.name.startswith("sp001.infrastructure")
                for alias in node.names
            )
        if isinstance(node, ast.Attribute):
            assert node.attr not in {"_store", "_completer"}
