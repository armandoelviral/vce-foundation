from collections.abc import Mapping
import json
import os
from pathlib import Path
import re

from cryptography.hazmat.primitives.serialization import load_pem_public_key

from sp001.infrastructure.case_state_host_composition import compose_case_state_host
from sp001.infrastructure.jwt_case_access_authenticator import JwtCaseAccessAuthenticator
from sp001.services.local_case_state_reader import LocalCaseStateReader
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate public key identifier")
        result[key] = value
    return result


def create_app_from_environment(*, environment: Mapping[str, str]):
    """Validate explicit configuration, then construct the authenticated host."""
    def required(name):
        value = environment.get(name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} is required")
        if value != value.strip():
            raise ValueError(f"{name} must not contain surrounding whitespace")
        return value

    def positive_integer(name):
        value = required(name)
        if re.fullmatch(r"[0-9]+", value) is None or int(value) <= 0:
            raise ValueError(f"{name} must be a positive decimal integer")
        return int(value)

    def absolute_path(name):
        value = Path(required(name))
        if not value.is_absolute():
            raise ValueError(f"{name} must be an absolute path")
        return value.resolve()

    issuer = required("SP001_AUTH_ISSUER")
    audience = required("SP001_AUTH_AUDIENCE")
    lifetime = positive_integer("SP001_AUTH_MAX_LIFETIME_SECONDS")
    token_limit = positive_integer("SP001_AUTH_MAX_TOKEN_BYTES")
    keys_path = absolute_path("SP001_AUTH_PUBLIC_KEYS_FILE")
    case_path = absolute_path("SP001_CASE_DATABASE_PATH")
    grants_path = absolute_path("SP001_GRANTS_DATABASE_PATH")

    if len({keys_path, case_path, grants_path}) != 3:
        raise ValueError("key file and database paths must be distinct")
    if not keys_path.is_file():
        raise ValueError("public keys file must exist")
    for path in (case_path, grants_path):
        if not path.parent.is_dir():
            raise ValueError("database parent directory must exist")
        if path.exists() and not path.is_file():
            raise ValueError("database path must identify a regular file")
    existing = [path for path in (keys_path, case_path, grants_path) if path.exists()]
    for index, first in enumerate(existing):
        for second in existing[index + 1:]:
            if first.samefile(second):
                raise ValueError("configured paths must not share the same file")

    raw_keys = json.loads(
        keys_path.read_text(), object_pairs_hook=_unique_object
    )
    if not isinstance(raw_keys, dict) or not raw_keys:
        raise ValueError("public keys file must contain a nonempty JSON object")
    keys = {}
    for kid, pem in raw_keys.items():
        if not isinstance(pem, str):
            raise TypeError("public key values must be PEM strings")
        keys[kid] = load_pem_public_key(pem.encode("ascii"))

    # Validate key types, issuer, audience and verifier limits before persistence.
    JwtCaseAccessAuthenticator(
        issuer=issuer, audience=audience, public_keys=keys,
        max_lifetime_seconds=lifetime, max_token_bytes=token_limit,
    )
    store = SqliteCaseAuthoritativeStateStore(database_path=case_path)
    return compose_case_state_host(
        reader=LocalCaseStateReader(store=store),
        issuer=issuer, audience=audience, public_keys=keys,
        max_lifetime_seconds=lifetime, max_token_bytes=token_limit,
        grants_database_path=grants_path,
    )


def create_app():
    """Uvicorn factory: importing this module creates no application or database."""
    return create_app_from_environment(environment=dict(os.environ))
