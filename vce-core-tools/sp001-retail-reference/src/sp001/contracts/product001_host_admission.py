
from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.isk_isolation_preconditions import (
    IsolationPreconditions,
    PreconditionStatus,
)

REQUIRED_CHECK_IDS = frozenset(
    f"HOST-P{i:02d}" for i in range(1, 11)
)


class HostAdmissionStatus(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    REJECTED = "REJECTED"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class HostAdmissionAssessment:
    status: HostAdmissionStatus
    failed_check_ids: tuple[str, ...]
    unknown_check_ids: tuple[str, ...]


def assess_product001_host_admission(
    preconditions: IsolationPreconditions,
) -> HostAdmissionAssessment:
    if type(preconditions) is not IsolationPreconditions:
        raise TypeError(
            "preconditions must be IsolationPreconditions"
        )

    checks = {
        check.check_id: check
        for check in preconditions.checks
    }

    if set(checks) != REQUIRED_CHECK_IDS:
        raise ValueError(
            "host precondition coverage mismatch"
        )

    failed = tuple(
        sorted(
            check_id
            for check_id, check in checks.items()
            if check.status is PreconditionStatus.FAILED
        )
    )

    unknown = tuple(
        sorted(
            check_id
            for check_id, check in checks.items()
            if check.status is PreconditionStatus.UNKNOWN
        )
    )

    if failed:
        status = HostAdmissionStatus.REJECTED
    elif unknown:
        status = HostAdmissionStatus.INDETERMINATE
    else:
        status = HostAdmissionStatus.ELIGIBLE

    return HostAdmissionAssessment(
        status=status,
        failed_check_ids=failed,
        unknown_check_ids=unknown,
    )
