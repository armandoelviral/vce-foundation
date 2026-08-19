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

    def __post_init__(self) -> None:
        if (
            not isinstance(self.dimension_id, str)
            or not self.dimension_id.strip()
        ):
            raise ValueError(
                "dimension_id must not be empty"
            )

        if (
            not isinstance(self.dimension_type, str)
            or not self.dimension_type.strip()
        ):
            raise ValueError(
                "dimension_type must not be empty"
            )

        if not isinstance(
            self.applicability,
            DimensionApplicability,
        ):
            raise TypeError(
                "applicability must be a "
                "DimensionApplicability"
            )

        if not isinstance(
            self.evidence_status,
            DimensionEvidenceStatus,
        ):
            raise TypeError(
                "evidence_status must be a "
                "DimensionEvidenceStatus"
            )

        if (
            self.applicability
            is DimensionApplicability.NOT_APPLICABLE
            and self.value is not None
        ):
            raise ValueError(
                "NOT_APPLICABLE dimensions "
                "cannot contain a value"
            )

        if (
            self.evidence_status
            is DimensionEvidenceStatus.NOT_PROVIDED
            and self.value is not None
        ):
            raise ValueError(
                "NOT_PROVIDED evidence "
                "cannot contain a value"
            )

        supported_evidence = {
            DimensionEvidenceStatus.DOCUMENTED,
            DimensionEvidenceStatus.HUMAN_DECLARED,
            DimensionEvidenceStatus.MEASURED,
            DimensionEvidenceStatus.INDEPENDENTLY_VERIFIED,
        }

        if (
            self.evidence_status in supported_evidence
            and self.value is None
        ):
            raise ValueError(
                "documented evidence requires a value"
            )
