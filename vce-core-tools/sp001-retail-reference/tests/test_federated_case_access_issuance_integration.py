from dataclasses import replace
import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from test_sqlite_case_access_issuance_preparations import setup
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
)
from sp001.contracts.case_access_issuance_preparation import IssuanceGrantReference
from sp001.infrastructure.configured_access_token_keys import ConfiguredAccessTokenKeys
from sp001.infrastructure.jwt_federated_issuance_authenticator import (
    JwtFederatedIssuanceAuthenticator,
)
from sp001.infrastructure.prepared_case_access_credentials import (
    PreparedCaseAccessSigner, PreparedCredentialProtector,
)
from sp001.infrastructure.sqlite_case_access_issuance_completions import (
    SqliteCaseAccessIssuanceCompletions, PreparedCaseAccessCompleter,
)
from sp001.services.authenticated_case_access_issuance import (
    AuthenticatedCaseAccessIssuance,
    IssuanceAuthenticationRejected, IssuanceIdentityRejected,
)
from sp001.services.case_access_issuance_reference_validation import (
    IssuanceReferenceValidationError,
)


@pytest.fixture
def flow(tmp_path):
    path, _, binding, command, template = setup(tmp_path)
    now = int(time.time())
    store = SqliteCaseAccessIssuanceCompletions(database_path=path)
    grant = replace(
        command.grant, grant_id="LIVE-GRANT",
        valid_from=now - 10, expires_at=now + 600,
    )
    command = replace(
        command, event_id="LIVE-GRANT-CREATE", grant=grant, recorded_at=now,
    )
    store.apply(record=command)
    preparation = replace(
        template, request_id="LIVE-REQUEST",
        payload=replace(
            template.payload, token_id="LIVE-TOKEN",
            issued_at=now - 1, not_before=now - 1, expires_at=now + 120,
        ),
        grant_references=(
            IssuanceGrantReference(
                grant.grant_id, 1, grant.permission, grant.expires_at,
            ),
        ),
    )
    primary_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    access_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    authenticator = JwtFederatedIssuanceAuthenticator(
        issuer="external", audience="issuance-service",
        key_resolver=ConfiguredAccessTokenKeys(
            issuer="external", public_keys={"PRIMARY-1": primary_key.public_key()},
        ),
        max_lifetime_seconds=300, max_token_bytes=8192,
    )
    completer = PreparedCaseAccessCompleter(
        store=store,
        signer=PreparedCaseAccessSigner(
            signing_key_id="KEY-1", private_key=access_key,
            issuer="access", audience="coordinator",
        ),
        protector=PreparedCredentialProtector(
            protection_key_id="PROTECTION-1", key=b"x" * 32,
        ),
    )
    service = AuthenticatedCaseAccessIssuance(
        authenticator=authenticator, backend=completer,
        expected_audience="issuance-service",
    )

    def primary(**changes):
        claims = {
            "iss": "external", "sub": "external-subject",
            "aud": "issuance-service",
            "iat": now - 1, "nbf": now - 1, "exp": now + 180,
        }
        claims.update(changes)
        return jwt.encode(
            claims, primary_key, algorithm="RS256",
            headers={"kid": "PRIMARY-1", "typ": "at+jwt"},
        )

    return store, service, preparation, command, primary, access_key


def test_real_primary_jwt_reaches_durable_completion_and_recovery(flow):
    store, service, preparation, _, primary, access_key = flow
    credential = primary()
    assert service.prepare(
        credential=credential, preparation=preparation,
    ) == preparation
    token = service.complete(
        credential=credential, request_id=preparation.request_id,
    )
    claims = jwt.decode(
        token.credential, access_key.public_key(), algorithms=["RS256"],
        issuer="access", audience="coordinator",
    )
    assert claims == preparation.payload.to_claims()
    historical = store.read_completed(request_id=preparation.request_id)
    assert historical is not None
    assert service.complete(
        credential=primary(), request_id=preparation.request_id,
    ) == token
    assert store.read_completed(request_id=preparation.request_id) == historical


@pytest.mark.parametrize("changes, error", [
    ({"aud": "coordinator"}, IssuanceAuthenticationRejected),
    ({"iss": "other"}, IssuanceAuthenticationRejected),
    ({"sub": "other"}, IssuanceIdentityRejected),
])
def test_rejected_primary_cannot_prepare(flow, changes, error):
    store, service, preparation, _, primary, _ = flow
    with pytest.raises(error):
        service.prepare(credential=primary(**changes), preparation=preparation)
    assert store.read_prepared(request_id=preparation.request_id) is None
    assert store.read_completed(request_id=preparation.request_id) is None


def test_real_primary_cannot_recover_after_grant_revocation(flow):
    store, service, preparation, command, primary, _ = flow
    credential = primary()
    service.prepare(credential=credential, preparation=preparation)
    service.complete(credential=credential, request_id=preparation.request_id)
    historical = store.read_completed(request_id=preparation.request_id)
    store.apply(record=replace(
        command, event_id="LIVE-REVOKE", action=Action.REVOKE,
    ))
    with pytest.raises(IssuanceReferenceValidationError):
        service.complete(credential=credential, request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) == historical
