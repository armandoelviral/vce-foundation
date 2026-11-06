from sp001.contracts.case_access_context import CaseAccessOperation as Operation
from sp001.contracts.retail_observation_operation import (
    RetailObservationSaveRequest as Request,
    RetailObservationOperationIdentity as Identity,
    RetailObservationOperationReceipt as Receipt,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    deserialize_retail_inspection_observation as deserialize,
)
from sp001.services.authenticated_inspection_observations import (
    AuthenticatedInspectionObservations,
)
from sp001.services.retail_observation_operation_validation import (
    validate_retail_observation_operation as validate,
)


class AuthenticatedObservationOperations(AuthenticatedInspectionObservations):
    """Authenticate operation access; do not establish inspection authorship.

    Backend failures propagate. A save exception may follow a successful commit.
    Operation recovery is scoped to the authenticated principal and exact case.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for name in ("save_operation_authorized", "recover_operation_authorized"):
            if not callable(getattr(self._backend, name, None)):
                raise TypeError("backend must provide observation operations")

    def save_operation(self, *, credential, request, photo=None):
        if type(request) is not Request:
            raise TypeError("request must be an observation save request")
        access = self._authenticate(credential)
        self._check(
            access, request.observation.case_id, Operation.SAVE_RETAIL_OBSERVATION,
        )
        options = {} if photo is None else {"photo": photo}
        receipt = self._backend.save_operation_authorized(
            access=access, request=request, **options,
        )
        self._check(
            access, request.observation.case_id, Operation.SAVE_RETAIL_OBSERVATION,
        )
        validate(request=request, receipt=receipt, principal=access.principal)
        return receipt

    def recover_operation(
        self, *, credential, case_id, request_id, include_photo=False,
    ):
        if type(include_photo) is not bool:
            raise TypeError("include_photo must be a bool")
        access = self._authenticate(credential)
        identity = Identity(access.principal, case_id, request_id)
        self._check(access, case_id, Operation.READ_RETAIL_OBSERVATION)
        options = {"include_photo": True} if include_photo else {}
        result = self._backend.recover_operation_authorized(
            access=access, identity=identity, **options,
        )
        self._check(access, case_id, Operation.READ_RETAIL_OBSERVATION)
        if result is None:
            return None
        if include_photo:
            if type(result) is not tuple or len(result) != 2:
                raise TypeError("backend returned an invalid receipt and photo pair")
            receipt, photo = result
            if photo is not None and (type(photo) is not bytes or not photo):
                raise TypeError("backend returned invalid photo bytes")
        else:
            receipt = result
        if type(receipt) is not Receipt:
            raise TypeError("backend returned an invalid operation receipt")
        if receipt.operation != identity:
            raise ValueError("backend returned another operation identity")
        observation = deserialize(receipt.stored_observation.document)
        validate(
            request=Request(request_id, observation),
            receipt=receipt, principal=access.principal,
        )
        return (receipt, photo) if include_photo else receipt
