from sp001.contracts.case_access_context import (
    CaseAccessOperation,
    CaseAccessPermission,
    ValidatedCaseAccessContext,
)


def required_retail_report_permissions(
    *, case_id: str, recover_only: bool,
) -> tuple[CaseAccessPermission, ...]:
    """Exact case permissions for save-and-return or recovery."""
    if type(recover_only) is not bool:
        raise TypeError("recover_only must be an exact bool")
    read = CaseAccessPermission(
        case_id, CaseAccessOperation.READ_RETAIL_REPORT,
    )
    if recover_only:
        return (read,)
    return (
        CaseAccessPermission(case_id, CaseAccessOperation.SAVE_RETAIL_REPORT),
        read,
    )


def token_allows_retail_report(
    *,
    access: ValidatedCaseAccessContext,
    case_id: str,
    expected_audience: str,
    at_time: int,
    recover_only: bool,
) -> bool:
    """Check attributed claims only; no signature or current-grant validation."""
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
    required = required_retail_report_permissions(
        case_id=case_id, recover_only=recover_only,
    )
    return (
        access.audience == expected_audience
        and access.issued_at <= access.not_before <= at_time < access.expires_at
        and all(permission in access.permissions for permission in required)
    )
