from dataclasses import replace

import jwt
import pytest

from test_case_access_issuer_composition import configuration
from test_federated_case_access_issuance_integration import flow
from test_federated_jwks_https import jwks_host, resolver, primary
from sp001.contracts.case_access_grant_administration import GrantAdministrationAction
from sp001.contracts.case_access_issuance_request import CaseAccessIssuanceRequest
from sp001.infrastructure.case_access_issuer_composition import (
    compose_case_access_issuer_with_capabilities,
)
from sp001.infrastructure.prepared_case_access_credentials import (
    PreparedCaseAccessSigner, PreparedCredentialProtector,
)
from sp001.services.case_access_issuance_reference_validation import (
    IssuanceReferenceValidationError,
)


def capabilities(configuration, events):
    values = dict(configuration)
    signer = PreparedCaseAccessSigner(
        signing_key_id=values["signing_key_id"],
        private_key=values.pop("signing_private_key"),
        issuer=values["access_issuer"], audience=values["access_audience"],
    )
    protector = PreparedCredentialProtector(
        protection_key_id=values.pop("protection_key_id"),
        key=values.pop("protection_key"),
    )

    class Signer:
        def sign(self, *, preparation):
            events.append("sign")
            return signer.sign(preparation=preparation)

    class Protector:
        def protect(self, *, preparation, token):
            events.append("protect")
            return protector.protect(preparation=preparation, token=token)

        def recover(self, *, preparation, protected):
            events.append("recover")
            return protector.recover(
                preparation=preparation, protected=protected,
            )

    return dict(values, signer=Signer(), protector=Protector())


@pytest.mark.parametrize("change", [
    {"signer": object()},
    {"protector": object()},
    {"primary_audience": ""},
    {"max_access_lifetime_seconds": 0},
    {"authorization_database_path": "relative.sqlite3"},
    {"clock": 123},
])
def test_invalid_configuration_opens_no_database(configuration, change):
    events = []
    values = capabilities(configuration, events)
    path = configuration["authorization_database_path"]
    values.update(change)
    with pytest.raises((TypeError, ValueError)):
        compose_case_access_issuer_with_capabilities(**values)
    assert not path.exists()
    assert events == []


def test_injected_capabilities_issue_reopen_and_reject_revoked_recovery(
    configuration, flow, jwks_host, tmp_path,
):
    store, _, template, command, _, access_key = flow
    configuration.update(
        primary_key_resolver=resolver(jwks_host),
        signing_private_key=access_key,
        authorization_database_path=tmp_path / "authorization.sqlite3",
    )
    events = []
    values = capabilities(configuration, events)
    issuer = compose_case_access_issuer_with_capabilities(**values)
    assert events == []
    assert not hasattr(issuer, "prepare")

    credential = primary(jwks_host[2])
    request = CaseAccessIssuanceRequest(
        "INJECTED-REQUEST", "CASE-001",
        template.payload.permissions[0].operation,
    )
    prepared = issuer.prepare_request(credential=credential, request=request)
    token = issuer.complete(
        credential=credential, request_id=request.request_id,
    )
    assert jwt.decode(
        token.credential, access_key.public_key(), algorithms=["RS256"],
        issuer="access", audience="coordinator",
    ) == prepared.payload.to_claims()
    assert events == ["sign", "protect", "recover"]
    historical = store.read_completed(request_id=request.request_id)
    assert historical is not None

    reopened = compose_case_access_issuer_with_capabilities(**values)
    assert reopened.complete(
        credential=credential, request_id=request.request_id,
    ) == token
    assert events == ["sign", "protect", "recover", "recover"]
    assert store.read_completed(request_id=request.request_id) == historical

    store.apply(record=replace(
        command, event_id="INJECTED-REVOKE",
        action=GrantAdministrationAction.REVOKE,
    ))
    with pytest.raises(IssuanceReferenceValidationError):
        reopened.complete(
            credential=credential, request_id=request.request_id,
        )
    assert events == ["sign", "protect", "recover", "recover"]
    assert store.read_completed(request_id=request.request_id) == historical
