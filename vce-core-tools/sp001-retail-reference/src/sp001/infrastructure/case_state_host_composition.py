from collections.abc import Mapping
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from fastapi import FastAPI

from sp001.contracts.case_state_reader import CaseStateReader
from sp001.infrastructure.authenticated_case_state_http_host import (
    create_authenticated_case_state_app,
)
from sp001.infrastructure.jwt_case_access_authenticator import (
    JwtCaseAccessAuthenticator,
)
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.services.configured_case_access_grants import (
    GrantBackedCaseReadAuthorizer,
)


def compose_case_state_host(
    *,
    reader: CaseStateReader,
    issuer: str,
    audience: str,
    public_keys: Mapping[str, RSAPublicKey],
    max_lifetime_seconds: int,
    max_token_bytes: int,
    grants_database_path: str | Path,
) -> FastAPI:
    """Compose authenticated reads with current local persistent grants.

    No token issuance, default grants or public administration endpoint.
    """
    if not isinstance(reader, CaseStateReader):
        raise TypeError("reader must implement CaseStateReader")
    # Validate verifier configuration before opening the grants database.
    authenticator = JwtCaseAccessAuthenticator(
        issuer=issuer,
        audience=audience,
        public_keys=public_keys,
        max_lifetime_seconds=max_lifetime_seconds,
        max_token_bytes=max_token_bytes,
    )
    grants = SqliteCaseAccessGrants(database_path=grants_database_path)
    authorizer = GrantBackedCaseReadAuthorizer(grants=grants)
    return create_authenticated_case_state_app(
        reader=reader,
        authenticator=authenticator,
        authorizer=authorizer,
        expected_audience=audience,
    )
