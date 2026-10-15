import pytest

from test_case_access_issuance_completion import components
from test_authenticated_case_access_issuance import boundary
from test_case_access_issuer_composition import configuration
from sp001.contracts.case_access_issuer import CaseAccessIssuer
from sp001.infrastructure.case_access_issuer_composition import (
    compose_case_access_issuer,
)
from sp001.services.authenticated_case_access_issuance import (
    IssuanceAuthenticationRejected,
)
from sp001.services.case_access_issuer_facade import CaseAccessIssuerFacade


def test_composition_returns_narrow_authorized_facade(configuration):
    issuer = compose_case_access_issuer(**configuration)
    assert isinstance(issuer, CaseAccessIssuerFacade)
    assert isinstance(issuer, CaseAccessIssuer)
    methods = {
        name for name in dir(issuer)
        if not name.startswith("_") and callable(getattr(issuer, name))
    }
    assert methods == {"prepare_request", "complete"}
    assert not hasattr(issuer, "__dict__")
    for name in ("prepare", "confirm", "sign", "recover",
                 "store", "signer", "protector", "backend"):
        assert not hasattr(issuer, name)


def test_recovery_authenticates_every_call(components):
    preparation = components[4]
    service, authenticator = boundary(
        components, preparation.binding.external_principal,
    )
    issuer = CaseAccessIssuerFacade(service=service)
    token = issuer.complete(
        credential="primary", request_id=preparation.request_id,
    )
    assert issuer.complete(
        credential="renewed", request_id=preparation.request_id,
    ) == token
    authenticator.principal = None
    with pytest.raises(IssuanceAuthenticationRejected):
        issuer.complete(
            credential="invalid", request_id=preparation.request_id,
        )
    assert authenticator.calls == ["primary", "renewed", "invalid"]


def test_raw_preparation_is_not_exposed(components):
    service, _ = boundary(
        components, components[4].binding.external_principal,
    )
    issuer = CaseAccessIssuerFacade(service=service)
    with pytest.raises(AttributeError):
        issuer.prepare(credential="primary", preparation=components[4])
