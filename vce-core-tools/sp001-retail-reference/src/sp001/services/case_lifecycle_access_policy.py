from sp001.contracts.case_access_context import (
    CaseAccessOperation, CaseAccessPermission, ValidatedCaseAccessContext,
)
from sp001.contracts.case_lifecycle_request import (
    CaseOpeningRequest, CaseTransitionRequest,
)


def required_case_lifecycle_permissions(*, request, recover_only: bool):
    """Permissions required to execute-and-return or recover a result."""
    if type(request) not in (CaseOpeningRequest, CaseTransitionRequest):
        raise TypeError("request must be an exact lifecycle request")
    if type(recover_only) is not bool:
        raise TypeError("recover_only must be an exact bool")
    read = CaseAccessPermission(
        request.case_id, CaseAccessOperation.READ_LIFECYCLE_RESULT,
    )
    if recover_only:
        return (read,)
    operation = (
        CaseAccessOperation.OPEN_CASE
        if type(request) is CaseOpeningRequest
        else CaseAccessOperation.APPLY_CASE_TRANSITION
    )
    return (CaseAccessPermission(request.case_id, operation), read)


def token_allows_case_lifecycle(
    *, access, request, expected_audience: str,
    at_time: int, recover_only: bool,
) -> bool:
    """Check attributed claims only; no signature or current-grant validation."""
    if not isinstance(access, ValidatedCaseAccessContext):
        raise TypeError("access must be a ValidatedCaseAccessContext")
    if not isinstance(expected_audience, str) or not expected_audience.strip():
        raise ValueError("expected_audience must be a nonempty string")
    if type(at_time) is not int:
        raise TypeError("at_time must be integer Unix seconds")
    if at_time < 0:
        raise ValueError("at_time must be nonnegative")
    required = required_case_lifecycle_permissions(
        request=request, recover_only=recover_only,
    )
    return (
        access.audience == expected_audience
        and access.issued_at <= access.not_before <= at_time < access.expires_at
        and all(permission in access.permissions for permission in required)
    )
