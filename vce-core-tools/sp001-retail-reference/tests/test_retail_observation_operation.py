from dataclasses import FrozenInstanceError, replace

import pytest

from test_retail_inspection_observation import observation
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationIdentity,
    StoredRetailInspectionObservation,
)
from sp001.contracts.retail_observation_operation import (
    RetailObservationSaveRequest as Request,
    RetailObservationOperationIdentity as Identity,
    RetailObservationOperationReceipt as Receipt,
    RetailObservationEffectDisposition as Disposition,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


def values():
    item = observation()
    request = Request("REQUEST-1", item)
    identity = Identity(
        AuthenticatedPrincipal("ISSUER", "SUBJECT"),
        item.case_id, request.request_id,
    )
    stored = StoredRetailInspectionObservation(
        RetailInspectionObservationIdentity(
            item.observation_id, item.observation_version,
        ),
        serialize(item),
    )
    return request, identity, stored


@pytest.mark.parametrize("disposition", list(Disposition))
def test_preserves_exact_content_without_claiming_commit(disposition):
    request, identity, stored = values()
    receipt = Receipt(identity, stored, disposition)
    assert request.observation is not None
    assert receipt.operation is identity
    assert receipt.stored_observation is stored
    assert receipt.disposition is disposition
    assert receipt == Receipt(identity, stored, disposition)
    assert not hasattr(receipt, "committed_at")
    assert not hasattr(receipt, "credential")


@pytest.mark.parametrize("field,value", [
    ("principal", AuthenticatedPrincipal("OTHER", "SUBJECT")),
    ("principal", AuthenticatedPrincipal("ISSUER", "OTHER")),
    ("case_id", "OTHER-CASE"),
    ("request_id", "OTHER-REQUEST"),
])
def test_operation_scope_fields_distinguish_identities(field, value):
    _, identity, _ = values()
    assert replace(identity, **{field: value}) != identity


@pytest.mark.parametrize("value", ["", " ", "A B", "A\nB", "A\tB",
                                        "A\x00B", "A\x7fB"])
def test_rejects_invalid_request_ids(value):
    request, identity, _ = values()
    with pytest.raises(ValueError):
        Request(value, request.observation)
    with pytest.raises(ValueError):
        replace(identity, request_id=value)


@pytest.mark.parametrize("value", [None, 1, True, b"REQUEST"])
def test_request_id_requires_text(value):
    request, identity, _ = values()
    with pytest.raises(TypeError):
        Request(value, request.observation)
    with pytest.raises(TypeError):
        replace(identity, request_id=value)


@pytest.mark.parametrize("field,value", [
    ("principal", "SUBJECT"),
    ("case_id", None),
    ("case_id", ""),
    ("case_id", "   "),
])
def test_rejects_invalid_operation_scope(field, value):
    _, identity, _ = values()
    with pytest.raises((TypeError, ValueError)):
        replace(identity, **{field: value})


@pytest.mark.parametrize("field,value", [
    ("operation", None),
    ("stored_observation", "document"),
    ("disposition", "CREATED"),
    ("disposition", None),
])
def test_receipt_requires_nominal_values(field, value):
    _, identity, stored = values()
    receipt = Receipt(identity, stored, Disposition.CREATED)
    with pytest.raises(TypeError):
        replace(receipt, **{field: value})


def test_request_requires_nominal_observation():
    with pytest.raises(TypeError):
        Request("REQUEST-1", object())


def test_values_are_frozen_and_slotted():
    request, identity, stored = values()
    receipt = Receipt(identity, stored, Disposition.CREATED)
    for item in (request, identity, receipt):
        assert not hasattr(item, "__dict__")
        with pytest.raises(FrozenInstanceError):
            setattr(item, next(iter(item.__dataclass_fields__)), None)
