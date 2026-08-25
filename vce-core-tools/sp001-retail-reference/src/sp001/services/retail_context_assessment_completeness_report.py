from dataclasses import dataclass

from sp001.contracts.retail_context_snapshot_completeness import (
    SnapshotCompletenessStatus,
)
from sp001.services.retail_context_assessment import (
    RetailContextAssessmentResult,
)


@dataclass(frozen=True, slots=True)
class RetailContextAssessmentCompletenessReport:
    """Sanitized projection of customer-defined context completeness."""

    case_id: str
    snapshot_id: str
    snapshot_version: int
    context_definition_id: str | None
    definition_version: int | None
    context_completeness_status: SnapshotCompletenessStatus
    required_dimension_types: tuple[str, ...]
    missing_required_dimension_types: tuple[str, ...]
    insufficient_evidence_dimension_types: tuple[str, ...]
    disputed_dimension_types: tuple[str, ...]


def build_retail_context_assessment_completeness_report(
    *,
    result: RetailContextAssessmentResult,
) -> RetailContextAssessmentCompletenessReport:
    """Project observed completeness without modifying canonical reports."""

    if not isinstance(
        result,
        RetailContextAssessmentResult,
    ):
        raise TypeError(
            "result must be a "
            "RetailContextAssessmentResult"
        )

    snapshot = result.snapshot
    completeness = result.context_completeness

    if completeness is None:
        definition = snapshot.context_definition

        return RetailContextAssessmentCompletenessReport(
            case_id=snapshot.case_id,
            snapshot_id=snapshot.snapshot_id,
            snapshot_version=snapshot.snapshot_version,
            context_definition_id=(
                definition.context_definition_id
                if definition is not None
                else None
            ),
            definition_version=(
                definition.definition_version
                if definition is not None
                else None
            ),
            context_completeness_status=(
                SnapshotCompletenessStatus.NOT_ESTABLISHED
            ),
            required_dimension_types=(),
            missing_required_dimension_types=(),
            insufficient_evidence_dimension_types=(),
            disputed_dimension_types=(),
        )

    return RetailContextAssessmentCompletenessReport(
        case_id=completeness.case_id,
        snapshot_id=completeness.snapshot_id,
        snapshot_version=completeness.snapshot_version,
        context_definition_id=(
            completeness.context_definition_id
        ),
        definition_version=(
            completeness.definition_version
        ),
        context_completeness_status=(
            completeness.status
        ),
        required_dimension_types=(
            completeness.required_dimension_types
        ),
        missing_required_dimension_types=(
            completeness.missing_required_dimension_types
        ),
        insufficient_evidence_dimension_types=(
            completeness.insufficient_evidence_dimension_types
        ),
        disputed_dimension_types=(
            completeness.disputed_dimension_types
        ),
    )
