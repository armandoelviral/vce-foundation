from dataclasses import replace

import pytest

from test_retail_observation_operation import values
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_observation_operation import (
    RetailObservationOperationReceipt as Receipt,
    RetailObservationEffectDisposition as Disposition,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)
from sp001.services.retail_observation_operation_validation import (
    validate_retail_observation_operation as validate,
    RetailObservationOperationMismatch as Mismatch,
)


def inputs(disposition=Disposition.CREATED):
    request, identity, stored = values()
    return dict(
        request=request,
        receipt=Receipt(identity, stored, disposition),
        principal=identity.principal,
    )


@pytest.mark.parametrize("disposition", list(Disposition))
def test_accepts_exact_correspondence_without_mutating_inputs(disposition):
    args = inputs(disposition)
    before = dict(args)
    assert validate(**args) is None
    assert args == before
    assert args["receipt"].disposition is disposition


@pytest.mark.parametrize("principal", [
    AuthenticatedPrincipal("OTHER", "SUBJECT"),
    AuthenticatedPrincipal("ISSUER", "OTHER"),
])
def test_rejects_another_authenticated_principal(principal):
    args = inputs()
    args["principal"] = principal
    with pytest.raises(Mismatch, match="principal"):
        validate(**args)


@pytest.mark.parametrize("field,value,reason", [
    ("request_id", "OTHER", "request identity"),
    ("case_id", "OTHER", "operation case"),
])
def test_rejects_receipt_for_another_operation(field, value, reason):
    args = inputs()
    receipt = args["receipt"]
    args["receipt"] = replace(
        receipt, operation=replace(receipt.operation, **{field: value}),
    )
    with pytest.raises(Mismatch, match=reason):
        validate(**args)


@pytest.mark.parametrize("field,value", [
    ("observation_id", "OTHER"),
    ("observation_version", 2),
])
def test_rejects_stored_key_document_disagreement(field, value):
    args = inputs()
    receipt = args["receipt"]
    stored = receipt.stored_observation
    args["receipt"] = replace(receipt, stored_observation=replace(
        stored, identity=replace(stored.identity, **{field: value}),
    ))
    with pytest.raises(Mismatch, match="stored identity"):
        validate(**args)


@pytest.mark.parametrize("field,value,reason", [
    ("case_id", "OTHER", "document case"),
    ("description", "Different supplied description.", "content"),
    ("scope", "Different scope.", "content"),
    ("observation_id", "OTHER", "content"),
    ("observation_version", 2, "content"),
])
def test_rejects_valid_but_different_document(field, value, reason):
    args = inputs()
    receipt = args["receipt"]
    stored = receipt.stored_observation
    item = replace(args["request"].observation, **{field: value})
    identity = replace(
        stored.identity,
        observation_id=item.observation_id,
        observation_version=item.observation_version,
    )
    args["receipt"] = replace(receipt, stored_observation=replace(
        stored, identity=identity, document=serialize(item),
    ))
    with pytest.raises(Mismatch, match=reason):
        validate(**args)


@pytest.mark.parametrize("document", ["{}", "null", "not JSON", "[]"])
def test_rejects_invalid_document(document):
    args = inputs()
    receipt = args["receipt"]
    args["receipt"] = replace(receipt, stored_observation=replace(
        receipt.stored_observation, document=document,
    ))
    with pytest.raises(ValueError):
        validate(**args)


def test_rejects_noncanonical_document():
    args = inputs()
    receipt = args["receipt"]
    stored = receipt.stored_observation
    args["receipt"] = replace(receipt, stored_observation=replace(
        stored, document=stored.document + "\n",
    ))
    with pytest.raises(ValueError):
        validate(**args)


@pytest.mark.parametrize("name", ["request", "receipt", "principal"])
@pytest.mark.parametrize("value", [None, {}, "declared"])
def test_requires_nominal_inputs(name, value):
    args = inputs()
    args[name] = value
    with pytest.raises(TypeError):
        validate(**args)
