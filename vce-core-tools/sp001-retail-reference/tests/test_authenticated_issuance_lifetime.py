from dataclasses import replace

import pytest

from test_case_access_issuance_completion import components
from sp001.contracts.federated_issuance_context import (
    ValidatedFederatedIssuanceContext,
)
from sp001.services.authenticated_case_access_issuance import (
    AuthenticatedCaseAccessIssuance, IssuanceAuthenticationRejected,
)


def boundary(components, now, audience="issuance-service"):
    _, store, _, _, preparation, _, _, completer = components
    context = ValidatedFederatedIssuanceContext(
        preparation.binding.external_principal, audience, 100, 100, 160,
    )

    class Authenticator:
        def authenticate(self, *, credential):
            return context

    return AuthenticatedCaseAccessIssuance(
        authenticator=Authenticator(), backend=completer,
        expected_audience="issuance-service", clock=lambda: now[0],
    )


def test_expiry_during_signature_rolls_back_completion(components, monkeypatch):
    _, store, _, _, preparation, signer, _, _ = components
    now = [150]
    service = boundary(components, now)
    original = signer.sign

    def delayed_sign(**kwargs):
        token = original(**kwargs)
        now[0] = 160
        return token

    monkeypatch.setattr(signer, "sign", delayed_sign)
    with pytest.raises(IssuanceAuthenticationRejected):
        service.complete(credential="primary", request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) is None


def test_expiry_during_recovery_prevents_delivery_but_preserves_commit(
    components, monkeypatch,
):
    _, store, _, _, preparation, _, protector, _ = components
    now = [150]
    service = boundary(components, now)
    original = protector.recover

    def delayed_recovery(**kwargs):
        token = original(**kwargs)
        now[0] = 160
        return token

    monkeypatch.setattr(protector, "recover", delayed_recovery)
    with pytest.raises(IssuanceAuthenticationRejected):
        service.complete(credential="primary", request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) is not None


def test_expired_primary_cannot_recover_confirmed_token(components):
    _, store, _, _, preparation, _, _, _ = components
    now = [150]
    service = boundary(components, now)
    service.complete(credential="primary", request_id=preparation.request_id)
    historical = store.read_completed(request_id=preparation.request_id)
    now[0] = 160
    with pytest.raises(IssuanceAuthenticationRejected):
        service.complete(credential="primary", request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) == historical


def test_wrong_audience_cannot_prepare(components):
    _, store, _, _, preparation, _, _, _ = components
    service = boundary(components, [150], audience="coordinator")
    new = replace(
        preparation, request_id="OTHER",
        payload=replace(preparation.payload, token_id="OTHER"),
    )
    with pytest.raises(IssuanceAuthenticationRejected):
        service.prepare(credential="primary", preparation=new)
    assert store.read_prepared(request_id="OTHER") is None
