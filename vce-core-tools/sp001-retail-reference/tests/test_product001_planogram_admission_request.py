import pytest

from sp001.contracts.product001_planogram_admission_request import (
    Product001PlanogramAdmissionRequest,
)


def make_request(**overrides):
    values = {
        "source_id": "PLANOGRAM-001",
        "source_version": 1,
        "point_of_sale_id": "STORE-001",
        "campaign_id": "CAMPAIGN-001",
    }
    values.update(overrides)
    return Product001PlanogramAdmissionRequest(**values)


def test_valid_commercial_request():
    request = make_request()

    assert request.source_id == "PLANOGRAM-001"
    assert request.source_version == 1
    assert request.point_of_sale_id == "STORE-001"
    assert request.campaign_id == "CAMPAIGN-001"


@pytest.mark.parametrize(
    "field",
    ("source_id", "point_of_sale_id", "campaign_id"),
)
@pytest.mark.parametrize("invalid", ("", " ", None, 123))
def test_invalid_identifiers_are_rejected(field, invalid):
    with pytest.raises((TypeError, ValueError)):
        make_request(**{field: invalid})


@pytest.mark.parametrize("invalid", (0, -1, True, "1", None))
def test_invalid_source_version_is_rejected(invalid):
    with pytest.raises((TypeError, ValueError)):
        make_request(source_version=invalid)


@pytest.mark.parametrize(
    "forbidden",
    (
        "retrieval_decision",
        "authority_bindings",
        "content",
        "effective_period",
        "supersession_graph",
        "source_status",
        "retrieval_context",
    ),
)
def test_authority_inputs_cannot_be_injected(forbidden):
    with pytest.raises(TypeError):
        make_request(**{forbidden: object()})


def test_request_is_immutable():
    request = make_request()

    with pytest.raises((AttributeError, TypeError)):
        request.source_id = "FORGED-PLANOGRAM"


def test_request_has_no_instance_dictionary():
    request = make_request()

    assert not hasattr(request, "__dict__")
