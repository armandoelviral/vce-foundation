from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.product001_document_version_binding import (
    Product001DocumentVersionBinding,
)


def make_binding(**overrides):
    values = {
        "source_id": "POG-2026-DENIM-012",
        "commercial_version": 1,
        "document_version": "current",
        "point_of_sale_id": "POS-045",
        "campaign_id": "CAMP-SPRING-2026",
    }
    values.update(overrides)
    return Product001DocumentVersionBinding(**values)


def test_explicit_version_binding():
    binding = make_binding()

    assert binding.commercial_version == 1
    assert binding.document_version == "current"


@pytest.mark.parametrize(
    "field",
    (
        "source_id",
        "document_version",
        "point_of_sale_id",
        "campaign_id",
    ),
)
def test_empty_identity_is_rejected(field):
    with pytest.raises((TypeError, ValueError)):
        make_binding(**{field: ""})


@pytest.mark.parametrize(
    "invalid",
    (0, -1, True, "1", None),
)
def test_invalid_commercial_version_is_rejected(invalid):
    with pytest.raises((TypeError, ValueError)):
        make_binding(commercial_version=invalid)


def test_binding_is_immutable():
    binding = make_binding()

    with pytest.raises(FrozenInstanceError):
        binding.document_version = "forged"


def test_binding_rejects_authority_injection():
    with pytest.raises(TypeError):
        make_binding(retrieval_decision=object())
