"""Tests for the internal PRODUCT-001 commercial composition."""

from pathlib import Path

import pytest

from sp001.infrastructure.jwt_federated_issuance_authenticator import (
    JwtFederatedIssuanceAuthenticator,
)
from sp001.infrastructure.product001_commercial_approval_composition import (
    compose_product001_commercial_approval,
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


class Resolver:
    def resolve(self, *, issuer, key_id, algorithm):
        return None


def configuration(tmp_path):
    root = tmp_path / "documents"
    root.mkdir()
    return {
        "issuer": "https://issuer.example",
        "audience": "product001-commercial",
        "key_resolver": Resolver(),
        "max_lifetime_seconds": 300,
        "max_token_bytes": 4096,
        "database_path": tmp_path / "commercial.sqlite",
        "documentary_storage_root": root,
        "clock": lambda: 100,
    }


def test_composition_uses_real_dependencies(tmp_path):
    config = configuration(tmp_path)

    service = compose_product001_commercial_approval(**config)

    assert isinstance(
        service, AuthenticatedProduct001CommercialApproval
    )
    assert isinstance(
        service._authenticator,
        JwtFederatedIssuanceAuthenticator,
    )
    assert isinstance(
        service._writer,
        SqliteProduct001CommercialDecisionWriter,
    )
    assert isinstance(
        service._document_verifier,
        Product001CommercialDocumentVerifier,
    )
    assert config["database_path"].is_file()


@pytest.mark.parametrize(
    "field,value",
    [
        ("issuer", ""),
        ("audience", ""),
        ("key_resolver", object()),
        ("max_lifetime_seconds", 0),
        ("max_token_bytes", 0),
        ("database_path", Path("relative.sqlite")),
        ("database_path", None),
        ("documentary_storage_root", Path("relative")),
        ("documentary_storage_root", None),
        ("clock", None),
    ],
)
def test_invalid_configuration_creates_no_database(
    tmp_path, field, value
):
    config = configuration(tmp_path)
    config[field] = value
    database_path = tmp_path / "commercial.sqlite"

    with pytest.raises((TypeError, ValueError)):
        compose_product001_commercial_approval(**config)

    assert not database_path.exists()


def test_missing_documentary_root_creates_no_database(tmp_path):
    config = configuration(tmp_path)
    config["documentary_storage_root"] = tmp_path / "missing"

    with pytest.raises(ValueError):
        compose_product001_commercial_approval(**config)

    assert not config["database_path"].exists()


def test_documentary_symlink_creates_no_database(tmp_path):
    config = configuration(tmp_path)
    alias = tmp_path / "documents-alias"
    alias.symlink_to(config["documentary_storage_root"])
    config["documentary_storage_root"] = alias

    with pytest.raises(ValueError):
        compose_product001_commercial_approval(**config)

    assert not config["database_path"].exists()


def test_database_parent_missing_creates_no_database(tmp_path):
    config = configuration(tmp_path)
    config["database_path"] = (
        tmp_path / "missing" / "commercial.sqlite"
    )

    with pytest.raises(ValueError):
        compose_product001_commercial_approval(**config)

    assert not config["database_path"].exists()


def test_invalid_resolver_rejected_before_storage(tmp_path):
    config = configuration(tmp_path)
    config["key_resolver"] = object()

    with pytest.raises(TypeError):
        compose_product001_commercial_approval(**config)

    assert not config["database_path"].exists()
