from sp001.contracts.case_access_context import (
    CaseAccessOperation,
    CaseAccessPermission,
    ValidatedCaseAccessContext,
)


def required_retail_observation_permissions(
    *, case_id: str, operation: CaseAccessOperation,
) -> tuple[CaseAccessPermission, ...]:
    """One exact case permission; save and read do not imply each other."""
    if not isinstance(operation, CaseAccessOperation):
        raise TypeError("operation must be a CaseAccessOperation")
    if operation not in (
        CaseAccessOperation.SAVE_RETAIL_OBSERVATION,
        CaseAccessOperation.READ_RETAIL_OBSERVATION,
    ):
        raise ValueError("operation is not an observation operation")
    return (CaseAccessPermission(case_id, operation),)


def token_allows_retail_observation(
    *,
    access: ValidatedCaseAccessContext,
    case_id: str,
    operation: CaseAccessOperation,
    expected_audience: str,
    at_time: int,
) -> bool:
    """Check attributed claims only, not signatures or current local grants.

    Constructing an access context establishes no authentication.
    This policy neither accesses storage nor verifies observer attribution.
    """
    if not isinstance(access, ValidatedCaseAccessContext):
        raise TypeError("access must be a ValidatedCaseAccessContext")
    if not isinstance(expected_audience, str):
        raise TypeError("expected_audience must be a string")
    if not expected_audience.strip():
        raise ValueError("expected_audience must not be empty")
    if type(at_time) is not int:
        raise TypeError("at_time must be integer Unix seconds")
    if at_time < 0:
        raise ValueError("at_time must be nonnegative")

    required = required_retail_observation_permissions(
        case_id=case_id, operation=operation,
    )
    return (
        access.audience == expected_audience
        and access.issued_at <= access.not_before <= at_time < access.expires_at
        and all(permission in access.permissions for permission in required)
    )
