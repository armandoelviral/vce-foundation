from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_context_dimension_evaluation import (
    DimensionEvaluationStatus,
    evaluate_context_dimension,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


class SnapshotCompletenessStatus(StrEnum):
    """Evidence availability for customer-required context dimensions."""

    NOT_ESTABLISHED = "NOT_ESTABLISHED"
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class SnapshotCompletenessResult:
    """Immutable evaluation of explicitly configured context requirements."""

    snapshot_id: str
    snapshot_version: int
    case_id: str
    context_definition_id: str | None
    definition_version: int | None
    status: SnapshotCompletenessStatus
    required_dimension_types: tuple[str, ...]
    missing_required_dimension_types: tuple[str, ...]
    insufficient_evidence_dimension_types: tuple[str, ...]
    disputed_dimension_types: tuple[str, ...]


def evaluate_retail_context_snapshot_completeness(
    *,
    snapshot: RetailContextSnapshot,
) -> SnapshotCompletenessResult:
    """Evaluate required dimension evidence without modifying its snapshot."""

    if not isinstance(
        snapshot,
        RetailContextSnapshot,
    ):
        raise TypeError(
            "snapshot must be a RetailContextSnapshot"
        )

    definition = snapshot.context_definition

    if definition is None:
        return SnapshotCompletenessResult(
            snapshot_id=snapshot.snapshot_id,
            snapshot_version=snapshot.snapshot_version,
            case_id=snapshot.case_id,
            context_definition_id=None,
            definition_version=None,
            status=(
                SnapshotCompletenessStatus.NOT_ESTABLISHED
            ),
            required_dimension_types=(),
            missing_required_dimension_types=(),
            insufficient_evidence_dimension_types=(),
            disputed_dimension_types=(),
        )

    classification_established = bool(
        definition.required_dimension_types
        or definition.optional_dimension_types
    )

    if not classification_established:
        return SnapshotCompletenessResult(
            snapshot_id=snapshot.snapshot_id,
            snapshot_version=snapshot.snapshot_version,
            case_id=snapshot.case_id,
            context_definition_id=(
                definition.context_definition_id
            ),
            definition_version=definition.definition_version,
            status=(
                SnapshotCompletenessStatus.NOT_ESTABLISHED
            ),
            required_dimension_types=(),
            missing_required_dimension_types=(),
            insufficient_evidence_dimension_types=(),
            disputed_dimension_types=(),
        )

    available_dimensions = {}

    for dimension in snapshot.dimensions:
        available_dimensions.setdefault(
            dimension.dimension_type,
            [],
        ).append(
            dimension,
        )

    missing_dimension_types = []
    insufficient_dimension_types = []
    disputed_dimension_types = []

    for dimension_type in (
        definition.required_dimension_types
    ):
        dimensions = available_dimensions.get(
            dimension_type,
        )

        if not dimensions:
            missing_dimension_types.append(
                dimension_type,
            )
            continue

        dimension_results = tuple(
            evaluate_context_dimension(
                dimension,
            )
            for dimension in dimensions
        )

        if any(
            result is DimensionEvaluationStatus.DISPUTED
            for result in dimension_results
        ):
            disputed_dimension_types.append(
                dimension_type,
            )
            continue

        if any(
            result is not DimensionEvaluationStatus.EVALUABLE
            for result in dimension_results
        ):
            insufficient_dimension_types.append(
                dimension_type,
            )

    if disputed_dimension_types:
        status = (
            SnapshotCompletenessStatus.INDETERMINATE
        )
    elif missing_dimension_types:
        status = (
            SnapshotCompletenessStatus.INCOMPLETE
        )
    elif insufficient_dimension_types:
        status = (
            SnapshotCompletenessStatus.INDETERMINATE
        )
    else:
        status = (
            SnapshotCompletenessStatus.COMPLETE
        )

    return SnapshotCompletenessResult(
        snapshot_id=snapshot.snapshot_id,
        snapshot_version=snapshot.snapshot_version,
        case_id=snapshot.case_id,
        context_definition_id=(
            definition.context_definition_id
        ),
        definition_version=definition.definition_version,
        status=status,
        required_dimension_types=(
            definition.required_dimension_types
        ),
        missing_required_dimension_types=tuple(
            missing_dimension_types,
        ),
        insufficient_evidence_dimension_types=tuple(
            insufficient_dimension_types,
        ),
        disputed_dimension_types=tuple(
            disputed_dimension_types,
        ),
    )
