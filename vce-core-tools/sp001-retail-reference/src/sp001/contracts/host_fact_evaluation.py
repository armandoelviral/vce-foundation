from dataclasses import dataclass
from enum import StrEnum


REQUIRED_FINDING_CODES = frozenset(
    {
        "ASSERTION_STRUCTURE",
        "OBSERVER_IDENTITY",
        "MANDATE_SCOPE",
        "CHALLENGE_BINDING",
        "OBSERVATION_FRESHNESS",
        "EVIDENCE_INTEGRITY",
        "ASSERTION_AUTHENTICITY",
        "POLICY_BINDING",
    }
)


class DeclaredFindingOutcome(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


def _require_identifier(field: str, value: object) -> None:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")


def _require_evidence_ids(value: object) -> None:
    if type(value) is not tuple:
        raise TypeError("evidence_ids must be an immutable tuple")

    seen = set()

    for evidence_id in value:
        _require_identifier("evidence_id", evidence_id)

        if evidence_id in seen:
            raise ValueError("duplicate evidence_id")

        seen.add(evidence_id)


@dataclass(frozen=True, slots=True)
class HostFactFinding:
    """Unverified, declarative finding without authority."""

    check_code: str
    outcome: DeclaredFindingOutcome
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_identifier("check_code", self.check_code)

        if self.check_code not in REQUIRED_FINDING_CODES:
            raise ValueError("unknown finding check_code")

        if type(self.outcome) is not DeclaredFindingOutcome:
            raise TypeError(
                "outcome must be a DeclaredFindingOutcome"
            )

        _require_evidence_ids(self.evidence_ids)


@dataclass(frozen=True, slots=True)
class HostFactEvaluation:
    """Structural evaluation record; not a trusted verdict."""

    evaluation_record_id: str
    assertion_id: str
    evaluation_id: str
    evaluator_id: str
    evaluated_at: int
    policy_version: str
    findings: tuple[HostFactFinding, ...]

    def __post_init__(self) -> None:
        for field in (
            "evaluation_record_id",
            "assertion_id",
            "evaluation_id",
            "evaluator_id",
            "policy_version",
        ):
            _require_identifier(field, getattr(self, field))

        if type(self.evaluated_at) is not int:
            raise TypeError("evaluated_at must be an integer")

        if self.evaluated_at < 0:
            raise ValueError("evaluated_at must be nonnegative")

        if type(self.findings) is not tuple:
            raise TypeError("findings must be an immutable tuple")

        if not self.findings:
            raise ValueError("findings must not be empty")

        seen = set()

        for finding in self.findings:
            if type(finding) is not HostFactFinding:
                raise TypeError(
                    "findings must contain HostFactFinding"
                )

            if finding.check_code in seen:
                raise ValueError("duplicate finding check_code")

            seen.add(finding.check_code)
