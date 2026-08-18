from dataclasses import dataclass
from enum import StrEnum


class DimensionApplicability(StrEnum):
    """Customer-declared applicability of a retail context dimension."""

    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    DISPUTED = "DISPUTED"


class DimensionEvidenceStatus(StrEnum):
    """Evidence classification for a retail context dimension."""

    DOCUMENTED = "DOCUMENTED"
    HUMAN_DECLARED = "HUMAN_DECLARED"
    MEASURED = "MEASURED"
    INDEPENDENTLY_VERIFIED = "INDEPENDENTLY_VERIFIED"
    NOT_PROVIDED = "NOT_PROVIDED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    DISPUTED = "DISPUTED"


@dataclass(frozen=True, slots=True)
class RetailContextDimension:
    """Immutable customer-configurable retail context dimension."""

    dimension_id: str
    dimension_type: str
    applicability: DimensionApplicability
    evidence_status: DimensionEvidenceStatus
    value: str | None = None
