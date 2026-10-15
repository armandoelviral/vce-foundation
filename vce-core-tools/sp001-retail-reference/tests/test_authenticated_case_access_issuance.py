from dataclasses import replace

import pytest

from test_case_access_issuance_completion import components
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.services.authenticated_case_access_issuance import (
    AuthenticatedCaseAccessIssuance,
    IssuanceAuthenticationRejected, IssuanceIdentityRejected,
)


from sp001.contracts.federated_issuance_context import (
    ValidatedFederatedIssuanceContext,
)


class Authenticator:
    def __init__(self, principal):
        self.principal = principal
        self.calls = []

    def authenticate(self, *, credential):
        self.calls.append(credential)
        if self.principal is None:
            return None
        return ValidatedFederatedIssuanceContext(
            self.principal, 'issuance-service', 100, 100, 200,
        )


def boundary(components, principal):
    _, store, _, _, _, _, _, completer = components
    authenticator = Authenticator(principal)
    service = AuthenticatedCaseAccessIssuance(
        authenticator=authenticator, backend=completer,
        expected_audience='issuance-service', clock=lambda: 150,
    )
    return service, authenticator


def test_matching_identity_prepares_completes_and_recovers(components):
    _, store, _, _, preparation, _, _, _ = components
    service, authenticator = boundary(
        components, preparation.binding.external_principal,
    )
    assert service.prepare(
        credential="primary", preparation=preparation,
    ) == preparation
    token = service.complete(credential="primary", request_id=preparation.request_id)
    assert service.complete(
        credential="renewed-primary", request_id=preparation.request_id,
    ) == token
    assert authenticator.calls == ["primary", "primary", "renewed-primary"]
    assert store.read_completed(request_id=preparation.request_id) is not None


@pytest.mark.parametrize("field", ["issuer", "subject"])
def test_other_identity_cannot_prepare_or_complete(components, field):
    _, store, _, _, preparation, _, _, _ = components
    foreign = replace(preparation.binding.external_principal, **{field: "OTHER"})
    service, _ = boundary(components, foreign)
    new_preparation = replace(
        preparation, request_id="REQUEST-OTHER",
        payload=replace(preparation.payload, token_id="TOKEN-OTHER"),
    )
    with pytest.raises(IssuanceIdentityRejected):
        service.prepare(credential="foreign", preparation=new_preparation)
    assert store.read_prepared(request_id="REQUEST-OTHER") is None
    with pytest.raises(IssuanceIdentityRejected):
        service.complete(credential="foreign", request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) is None


def test_confirmed_token_requires_authentication_and_owner_on_every_recovery(
    components,
):
    _, store, _, _, preparation, _, _, _ = components
    service, authenticator = boundary(
        components, preparation.binding.external_principal,
    )
    service.complete(credential="valid", request_id=preparation.request_id)
    historical = store.read_completed(request_id=preparation.request_id)
    authenticator.principal = None
    with pytest.raises(IssuanceAuthenticationRejected):
        service.complete(credential="expired", request_id=preparation.request_id)
    authenticator.principal = AuthenticatedPrincipal("external", "OTHER")
    with pytest.raises(IssuanceIdentityRejected):
        service.complete(credential="foreign", request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) == historical


def test_invalid_credential_does_not_read_preparation(components, monkeypatch):
    _, store, _, _, preparation, _, _, _ = components
    service, _ = boundary(components, None)

    def forbidden_read(**kwargs):
        raise AssertionError("authentication must precede storage read")

    monkeypatch.setattr(store, "read_prepared", forbidden_read)
    with pytest.raises(IssuanceAuthenticationRejected):
        service.complete(credential="invalid", request_id=preparation.request_id)


def test_provider_failure_is_not_authentication_rejection(components):
    service, authenticator = boundary(components, None)

    def failed_provider(**kwargs):
        raise RuntimeError("provider unavailable")

    authenticator.authenticate = failed_provider
    with pytest.raises(RuntimeError, match="provider unavailable"):
        service.complete(credential="primary", request_id="REQUEST-1")
