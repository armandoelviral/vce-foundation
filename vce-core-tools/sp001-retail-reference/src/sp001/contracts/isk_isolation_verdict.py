from dataclasses import dataclass
from enum import StrEnum


class IsolationVerdictStatus(StrEnum):
    OBSERVED_HOLD = "OBSERVED_HOLD"
    FALSIFIED = "FALSIFIED"
    INDETERMINATE = "INDETERMINATE"
    NOT_TESTED = "NOT_TESTED"


@dataclass(frozen=True, slots=True)
class IsolationVerdict:
    """Declared experimental verdict; grants no operational authority."""

    verdict_id: str
    experiment_id: str
    status: IsolationVerdictStatus
    observation_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("verdict_id", "experiment_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonempty string")

        if not isinstance(self.status, IsolationVerdictStatus):
            raise TypeError("status must be an IsolationVerdictStatus")

        for name in ("observation_ids", "evidence_ids"):
            values = getattr(self, name)

            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be an immutable tuple")

            seen = set()
            for value in values:
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"{name} contains an invalid identity")

                if value in seen:
                    raise ValueError(f"{name} contains duplicate identities")

                seen.add(value)

        conclusive = {
            IsolationVerdictStatus.OBSERVED_HOLD,
            IsolationVerdictStatus.FALSIFIED,
        }

        if self.status in conclusive:
            if not self.observation_ids or not self.evidence_ids:
                raise ValueError(
                    "conclusive verdict requires observations and evidence"
                )

        if self.status is IsolationVerdictStatus.NOT_TESTED:
            if self.observation_ids:
                raise ValueError(
                    "untested experiment must not reference observations"
                )
