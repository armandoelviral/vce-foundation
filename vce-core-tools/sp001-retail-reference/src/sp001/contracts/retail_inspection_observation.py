from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from sp001.contracts.retail_process_actor import RetailProcessActor


class RetailInspectionObservationMethod(StrEnum):
    """Declared observation method, without verification claims."""

    DIRECT_INSPECTION = "DIRECT_INSPECTION"
    EVIDENCE_REVIEW = "EVIDENCE_REVIEW"


@dataclass(frozen=True, slots=True)
class RetailInspectionObservation:
    """Declared descriptive observation, without a compliance verdict.

    Actor identity, timestamps and evidence references are supplied facts.
    Construction does not authenticate, verify evidence, persist, approve,
    establish coverage or grant authority.
    observed_at identifies the inspection or evidence review, not capture.
    recorded_at is the declared recording time, not a confirmed commit time.
    An empty limitations tuple means none were recorded, not none exist.
    """

    observation_id: str
    observation_version: int
    case_id: str
    subject_reference: str
    method: RetailInspectionObservationMethod
    description: str
    scope: str
    limitations: tuple[str, ...]
    declared_observer: RetailProcessActor
    observed_at: datetime
    recorded_at: datetime
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in (
            "observation_id", "case_id", "subject_reference",
            "description", "scope",
        ):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        if type(self.observation_version) is not int:
            raise TypeError("observation_version must be an integer")
        if self.observation_version < 1:
            raise ValueError("observation_version must be positive")

        if not isinstance(self.method, RetailInspectionObservationMethod):
            raise TypeError("method must be a RetailInspectionObservationMethod")
        if not isinstance(self.declared_observer, RetailProcessActor):
            raise TypeError("declared_observer must be a RetailProcessActor")

        for name in ("observed_at", "recorded_at"):
            value = getattr(self, name)
            if not isinstance(value, datetime):
                raise TypeError(f"{name} must be a datetime")
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{name} must be timezone-aware")

        if self.recorded_at < self.observed_at:
            raise ValueError("recorded_at must not precede observed_at")

        for name in ("limitations", "evidence_ids"):
            values = getattr(self, name)
            if type(values) is not tuple:
                raise TypeError(f"{name} must be a tuple")
            for value in values:
                if not isinstance(value, str):
                    raise TypeError(f"{name} items must be strings")
                if not value.strip():
                    raise ValueError(f"{name} items must not be empty")

        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("evidence_ids must be unique")
        if (
            self.method is RetailInspectionObservationMethod.EVIDENCE_REVIEW
            and not self.evidence_ids
        ):
            raise ValueError("evidence review requires evidence references")
