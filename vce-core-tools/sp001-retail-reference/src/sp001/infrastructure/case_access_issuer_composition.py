from sp001.contracts.case_access_issuer import CaseAccessIssuer
from sp001.services.case_access_issuer_facade import CaseAccessIssuerFacade
from collections.abc import Callable
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from sp001.contracts.access_token_key_resolver import AccessTokenKeyResolver
from sp001.contracts.case_access_issuance_policy import CaseAccessIssuancePolicy
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
)


def compose_case_access_issuer(
    *,
    primary_issuer: str,
    primary_audience: str,
    primary_key_resolver: AccessTokenKeyResolver,
    max_primary_lifetime_seconds: int,
    max_primary_token_bytes: int,
    access_issuer: str,
    access_audience: str,
    max_access_lifetime_seconds: int,
    signing_key_id: str,
    signing_private_key: RSAPrivateKey,
    protection_key_id: str,
    protection_key: bytes,
    authorization_database_path: str | Path,
    clock: Callable[[], int] | None = None,
) -> CaseAccessIssuer:
    """Compose internal issuance with explicit trust and injected key custody.

    No default bindings, grants, network discovery or public administration.
    """
    if clock is not None and not callable(clock):
        raise TypeError("clock must be callable")
    if not isinstance(authorization_database_path, (str, Path)):
        raise TypeError("authorization_database_path must be a string or Path")
    if not str(authorization_database_path).strip():
        raise ValueError("authorization_database_path must not be empty")
    path = Path(authorization_database_path)
    if not path.is_absolute():
        raise ValueError("authorization_database_path must be absolute")
    if not path.parent.is_dir() or (path.exists() and not path.is_file()):
        raise ValueError("authorization database requires an existing parent directory")

    authenticator = JwtFederatedIssuanceAuthenticator(
        issuer=primary_issuer, audience=primary_audience,
        key_resolver=primary_key_resolver,
        max_lifetime_seconds=max_primary_lifetime_seconds,
        max_token_bytes=max_primary_token_bytes,
    )
    signer = PreparedCaseAccessSigner(
        signing_key_id=signing_key_id, private_key=signing_private_key,
        issuer=access_issuer, audience=access_audience,
    )
    protector = PreparedCredentialProtector(
        protection_key_id=protection_key_id, key=protection_key,
    )
    policy = CaseAccessIssuancePolicy(
        primary_audience=primary_audience, access_issuer=access_issuer,
        access_audience=access_audience, signing_key_id=signing_key_id,
        max_lifetime_seconds=max_access_lifetime_seconds,
    )
    # All static security configuration is validated before opening storage.
    store = SqliteCaseAccessIssuanceCompletions(database_path=path)
    completer = PreparedCaseAccessCompleter(
        store=store, signer=signer, protector=protector, clock=clock,
    )
    service = AuthenticatedCaseAccessIssuance(
        authenticator=authenticator, backend=completer,
        expected_audience=primary_audience, clock=clock, issuance_policy=policy,
    )
    return CaseAccessIssuerFacade(service=service)
