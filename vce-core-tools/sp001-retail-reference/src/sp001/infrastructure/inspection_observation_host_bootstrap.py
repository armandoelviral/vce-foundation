import os
import time
from pathlib import Path

from cryptography.hazmat.primitives.serialization import load_pem_public_key

from sp001.infrastructure.configured_access_token_keys import (
    ConfiguredAccessTokenKeys,
)
from sp001.infrastructure.jwt_case_access_authenticator import (
    JwtCaseAccessAuthenticator,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    SqliteAuthorizedInspectionObservations,
)
from sp001.infrastructure.inspection_observation_read_http_host import (
    create_inspection_observation_read_app,
)
from sp001.services.authenticated_inspection_observations import (
    AuthenticatedInspectionObservations,
)


PREFIX = "SP001_INSPECTION_OBSERVATION_"


def create_app_from_environment(*, environment):
    """Compose exact-version observation recovery from explicit configuration.

    Requires an existing database; initializers may establish missing tables.
    Generates no credentials or grants and verifies no observer attribution.
    TLS and deployment configuration remain outside this factory.
    """
    def required(name):
        value = environment.get(PREFIX + name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"missing configuration: {PREFIX}{name}")
        return value

    def positive_integer(name):
        value = required(name)
        if not value.isascii() or not value.isdecimal():
            raise ValueError(f"invalid positive integer: {PREFIX}{name}")
        parsed = int(value)
        if parsed < 1:
            raise ValueError(f"invalid positive integer: {PREFIX}{name}")
        return parsed

    database = Path(required("DATABASE"))
    issuer = required("ISSUER")
    audience = required("AUDIENCE")
    key_id = required("KEY_ID")
    pem = required("PUBLIC_KEY_PEM")
    max_lifetime = positive_integer("MAX_LIFETIME_SECONDS")
    max_token_bytes = positive_integer("MAX_TOKEN_BYTES")

    if not database.is_file():
        raise ValueError("observation database must already exist")
    try:
        public_key = load_pem_public_key(pem.encode("ascii"))
    except (ValueError, TypeError, UnicodeError):
        raise ValueError("invalid public verification key") from None

    resolver = ConfiguredAccessTokenKeys(
        issuer=issuer, public_keys={key_id: public_key},
    )
    authenticator = JwtCaseAccessAuthenticator(
        issuer=issuer, audience=audience, key_resolver=resolver,
        max_lifetime_seconds=max_lifetime, max_token_bytes=max_token_bytes,
    )
    clock = lambda: int(time.time())
    backend = SqliteAuthorizedInspectionObservations(
        database_path=database, expected_audience=audience, clock=clock,
    )
    service = AuthenticatedInspectionObservations(
        authenticator=authenticator, backend=backend,
        expected_audience=audience, clock=clock,
    )
    return create_inspection_observation_read_app(
        service=service, max_token_bytes=max_token_bytes,
    )


def create_app():
    return create_app_from_environment(environment=os.environ)
