"""Internal fail-closed PRODUCT-001 commercial approval composition.

No host startup, network listener, endpoint or grant administration.
"""

from collections.abc import Callable
from pathlib import Path

from sp001.contracts.access_token_key_resolver import (
    AccessTokenKeyResolver,
)
from sp001.infrastructure.jwt_federated_issuance_authenticator import (
    JwtFederatedIssuanceAuthenticator,
)
from sp001.infrastructure.sqlite_product001_commercial_decisions import (
    SqliteProduct001CommercialDecisionWriter,
)
from sp001.services.authenticated_product001_commercial_approval import (
    AuthenticatedProduct001CommercialApproval,
)
from sp001.services.product001_commercial_document_verification import (
    Product001CommercialDocumentVerifier,
)


def compose_product001_commercial_approval(
    *,
    issuer: str,
    audience: str,
    key_resolver: AccessTokenKeyResolver,
    max_lifetime_seconds: int,
    max_token_bytes: int,
    database_path: Path,
    documentary_storage_root: Path,
    clock: Callable[[], int],
) -> AuthenticatedProduct001CommercialApproval:
    """Construct the internal approval service with real security dependencies."""

    # Validate security configuration before constructing SQLite storage.
    authenticator = JwtFederatedIssuanceAuthenticator(
        issuer=issuer,
        audience=audience,
        key_resolver=key_resolver,
        max_lifetime_seconds=max_lifetime_seconds,
        max_token_bytes=max_token_bytes,
    )

    if not isinstance(database_path, Path):
        raise TypeError("database_path must be a Path")
    if not database_path.is_absolute():
        raise ValueError("database_path must be absolute")
    if database_path.parent == database_path:
        raise ValueError("database_path must not be filesystem root")
    if not database_path.parent.is_dir():
        raise ValueError("database parent directory must exist")
    if database_path.exists() and not database_path.is_file():
        raise ValueError("database_path must reference a file")

    if not isinstance(documentary_storage_root, Path):
        raise TypeError("documentary_storage_root must be a Path")
    if not documentary_storage_root.is_absolute():
        raise ValueError("documentary_storage_root must be absolute")
    if (
        documentary_storage_root.parent
        == documentary_storage_root
    ):
        raise ValueError("documentary_storage_root must not be filesystem root")
    if not documentary_storage_root.is_dir():
        raise ValueError("documentary storage root must exist")
    if documentary_storage_root.is_symlink():
        raise ValueError("documentary storage root must not be a symlink")

    if not callable(clock):
        raise TypeError("clock must be callable")

    verifier = Product001CommercialDocumentVerifier(
        storage_root=documentary_storage_root,
    )

    writer = SqliteProduct001CommercialDecisionWriter(
        database_path=database_path,
        clock=clock,
    )

    return AuthenticatedProduct001CommercialApproval(
        authenticator=authenticator,
        writer=writer,
        document_verifier=verifier,
        expected_audience=audience,
        clock=clock,
    )
