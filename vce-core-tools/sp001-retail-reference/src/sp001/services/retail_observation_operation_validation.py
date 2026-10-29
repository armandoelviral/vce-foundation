from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_observation_operation import (
    RetailObservationSaveRequest,
    RetailObservationOperationReceipt,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    deserialize_retail_inspection_observation as deserialize,
    serialize_retail_inspection_observation as serialize,
)


class RetailObservationOperationMismatch(ValueError):
    """Supplied request, receipt and document do not describe the same effect."""


def validate_retail_observation_operation(
    *,
    request: RetailObservationSaveRequest,
    receipt: RetailObservationOperationReceipt,
    principal: AuthenticatedPrincipal,
) -> None:
    """Validate supplied correspondence only.

    Does not authenticate the principal, authorize access, establish CREATED
    versus REUSED, write, or prove commit. The caller must obtain the principal
    from its authenticated boundary. Codec failures propagate as validation
    failures, not as absence.
    """
    if type(request) is not RetailObservationSaveRequest:
        raise TypeError("request must be an observation save request")
    if type(receipt) is not RetailObservationOperationReceipt:
        raise TypeError("receipt must be an observation operation receipt")
    if type(principal) is not AuthenticatedPrincipal:
        raise TypeError("principal must be an AuthenticatedPrincipal")

    operation = receipt.operation
    expected = request.observation
    if operation.principal != principal:
        raise RetailObservationOperationMismatch("principal mismatch")
    if operation.request_id != request.request_id:
        raise RetailObservationOperationMismatch("request identity mismatch")
    if operation.case_id != expected.case_id:
        raise RetailObservationOperationMismatch("operation case mismatch")

    stored = receipt.stored_observation
    recovered = deserialize(stored.document)
    if (
        recovered.observation_id != stored.identity.observation_id
        or recovered.observation_version != stored.identity.observation_version
    ):
        raise RetailObservationOperationMismatch("stored identity mismatch")
    if recovered.case_id != operation.case_id:
        raise RetailObservationOperationMismatch("document case mismatch")
    if (
        recovered != expected
        or stored.document != serialize(expected)
    ):
        raise RetailObservationOperationMismatch("observation content mismatch")
