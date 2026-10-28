import os
import time
from pathlib import Path

from cryptography.hazmat.primitives.serialization import load_pem_public_key

from sp001.infrastructure.configured_access_token_keys import (
    ConfiguredAccessTokenKeys,
)
from sp001.infrastructure.retail_report_composition import (
    compose_transactional_retail_reports,
)
from sp001.infrastructure.retail_report_read_http_host import (
    create_retail_report_read_app,
)


PREFIX = "SP001_RETAIL_REPORT_"


def create_app_from_environment(*, environment):
    """Compose the read host from explicit configuration.

    Requires an existing database. Generates no credentials.
    Deployment and TLS configuration remain outside this factory.
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
        raise ValueError("report database must already exist")

    try:
        public_key = load_pem_public_key(pem.encode("ascii"))
    except (ValueError, TypeError, UnicodeError):
        raise ValueError("invalid public verification key") from None

    resolver = ConfiguredAccessTokenKeys(
        issuer=issuer,
        public_keys={key_id: public_key},
    )
    service = compose_transactional_retail_reports(
        issuer=issuer,
        audience=audience,
        key_resolver=resolver,
        max_lifetime_seconds=max_lifetime,
        max_token_bytes=max_token_bytes,
        database_path=database,
        clock=lambda: int(time.time()),
    )

    return create_retail_report_read_app(
        service=service,
        max_token_bytes=max_token_bytes,
    )


def create_app():
    return create_app_from_environment(environment=os.environ)
