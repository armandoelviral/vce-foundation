from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.observer_identity_certificate import (
    ObserverIdentityCertificate,
)


def certificate(**overrides):
    values = {
        "certificate_id": "CERT-001",
        "observer_id": "OBSERVER-001",
        "key_id": "KEY-001",
        "public_key_bytes": b"unverified-public-key",
        "platform_evidence_ids": ("EVIDENCE-001",),
    }
    values.update(overrides)
    return ObserverIdentityCertificate(**values)


def test_valid_record_preserves_exact_values():
    result = certificate()
    assert result.observer_id == "OBSERVER-001"
    assert result.public_key_bytes == b"unverified-public-key"


def test_record_is_immutable():
    result = certificate()
    with pytest.raises(FrozenInstanceError):
        result.observer_id = "OTHER"


@pytest.mark.parametrize(
    "field",
    ("certificate_id", "observer_id", "key_id"),
)
@pytest.mark.parametrize("invalid", ("", " ", None, 7))
def test_invalid_identity_is_rejected(field, invalid):
    with pytest.raises(ValueError):
        certificate(**{field: invalid})


@pytest.mark.parametrize("invalid", (None, "", bytearray(b"x"), 7))
def test_invalid_public_key_type_is_rejected(invalid):
    with pytest.raises(TypeError):
        certificate(public_key_bytes=invalid)


def test_empty_public_key_is_rejected():
    with pytest.raises(ValueError):
        certificate(public_key_bytes=b"")


@pytest.mark.parametrize("invalid", (None, [], "EVIDENCE-001"))
def test_invalid_evidence_collection_is_rejected(invalid):
    with pytest.raises(TypeError):
        certificate(platform_evidence_ids=invalid)


@pytest.mark.parametrize("invalid", ("", " ", None, 7))
def test_invalid_evidence_id_is_rejected(invalid):
    with pytest.raises(ValueError):
        certificate(platform_evidence_ids=(invalid,))


def test_duplicate_evidence_is_rejected():
    with pytest.raises(ValueError):
        certificate(
            platform_evidence_ids=("EVIDENCE-001", "EVIDENCE-001")
        )


def test_empty_evidence_collection_is_structurally_valid():
    assert certificate(platform_evidence_ids=()).platform_evidence_ids == ()


def test_construction_does_not_grant_authority():
    result = certificate()
    assert not hasattr(result, "trusted")
    assert not hasattr(result, "authorized")
    assert not hasattr(result, "verified")
    assert not hasattr(result, "eligible")


def test_replacement_preserves_validation():
    result = certificate()
    with pytest.raises(ValueError):
        replace(result, observer_id="")
