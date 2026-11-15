from dataclasses import dataclass
from enum import StrEnum


class PreconditionStatus(StrEnum):
    SATISFIED = "SATISFIED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class PreconditionCheck:
    check_id: str
    status: PreconditionStatus
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.check_id, str) or not self.check_id.strip():
            raise ValueError("check_id must be a nonempty string")

        if not isinstance(self.status, PreconditionStatus):
            raise TypeError("status must be a PreconditionStatus")

        if not isinstance(self.evidence_ids, tuple):
            raise TypeError("evidence_ids must be an immutable tuple")

        if self.status in (
            PreconditionStatus.SATISFIED,
            PreconditionStatus.FAILED,
        ) and not self.evidence_ids:
            raise ValueError("resolved precondition requires evidence")

        seen = set()
        for evidence_id in self.evidence_ids:
            if not isinstance(evidence_id, str) or not evidence_id.strip():
                raise ValueError("evidence_id must be a nonempty string")
            if evidence_id in seen:
                raise ValueError("duplicate evidence_id")
            seen.add(evidence_id)


@dataclass(frozen=True, slots=True)
class IsolationPreconditions:
    experiment_id: str
    checks: tuple[PreconditionCheck, ...]

    def __post_init__(self) -> None:
        if (
            not isinstance(self.experiment_id, str)
            or not self.experiment_id.strip()
        ):
            raise ValueError("experiment_id must be a nonempty string")

        if not isinstance(self.checks, tuple):
            raise TypeError("checks must be an immutable tuple")

        if not self.checks:
            raise ValueError("checks must not be empty")

        seen = set()
        for check in self.checks:
            if not isinstance(check, PreconditionCheck):
                raise TypeError("check must be a PreconditionCheck")
            if check.check_id in seen:
                raise ValueError("duplicate check_id")
            seen.add(check.check_id)
