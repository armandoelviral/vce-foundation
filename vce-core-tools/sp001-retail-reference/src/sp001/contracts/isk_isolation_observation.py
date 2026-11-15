from dataclasses import dataclass
from enum import StrEnum


class IsolationAttemptResult(StrEnum):
    DENIED = "DENIED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


class PersistentEffectStatus(StrEnum):
    UNCHANGED = "UNCHANGED"
    CHANGED = "CHANGED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class IsolationObservation:
    """Declared observations; establishes no isolation guarantee."""

    observation_id: str
    experiment_id: str
    attempt_id: str
    os_result: IsolationAttemptResult
    persistent_effect: PersistentEffectStatus
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        identities = {
            "observation_id": self.observation_id,
            "experiment_id": self.experiment_id,
            "attempt_id": self.attempt_id,
        }

        for name, value in identities.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonempty string")

        if not isinstance(self.os_result, IsolationAttemptResult):
            raise TypeError("os_result must be an IsolationAttemptResult")

        if not isinstance(self.persistent_effect, PersistentEffectStatus):
            raise TypeError(
                "persistent_effect must be a PersistentEffectStatus"
            )

        if not isinstance(self.evidence_ids, tuple):
            raise TypeError("evidence_ids must be an immutable tuple")

        seen = set()
        for evidence_id in self.evidence_ids:
            if not isinstance(evidence_id, str) or not evidence_id.strip():
                raise ValueError("evidence_id must be a nonempty string")
            if evidence_id in seen:
                raise ValueError("duplicate evidence_id")
            seen.add(evidence_id)

        if (
            self.os_result is not IsolationAttemptResult.UNKNOWN
            or self.persistent_effect is not PersistentEffectStatus.UNKNOWN
        ) and not self.evidence_ids:
            raise ValueError(
                "resolved observation requires evidence"
            )
