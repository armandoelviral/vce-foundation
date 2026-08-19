from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_context_dimension_evaluation import (
    DimensionEvaluationStatus,
    evaluate_context_dimension,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


class SnapshotEvaluationStatus(StrEnum):
    """Aggregated evaluation availability for a retail context snapshot."""

    EVALUABLE = "EVALUABLE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    DISPUTED = "DISPUTED"
    NO_DIMENSIONS = "NO_DIMENSIONS"


@dataclass(frozen=True, slots=True)
class SnapshotEvaluationResult:
    """Immutable snapshot evaluation preserving dimension-level outcomes."""

    snapshot_id: str
    snapshot_version: int
    case_id: str
    status: SnapshotEvaluationStatus
    dimension_results: tuple[
        tuple[str, DimensionEvaluationStatus],
        ...,
    ]


def evaluate_context_snapshot(
    snapshot: RetailContextSnapshot,
) -> SnapshotEvaluationResult:
    """Evaluate a snapshot without concealing individual dimension results."""

    if not isinstance(
        snapshot,
        RetailContextSnapshot,
    ):
        raise TypeError(
            "snapshot must be a RetailContextSnapshot"
        )

    dimension_results = tuple(
        (
            dimension.dimension_id,
            evaluate_context_dimension(dimension),
        )
        for dimension in snapshot.dimensions
    )

    if not dimension_results:
        status = SnapshotEvaluationStatus.NO_DIMENSIONS

    elif any(
        result is DimensionEvaluationStatus.DISPUTED
        for _, result in dimension_results
    ):
        status = SnapshotEvaluationStatus.DISPUTED

    elif any(
        result is DimensionEvaluationStatus.INSUFFICIENT_EVIDENCE
        for _, result in dimension_results
    ):
        status = SnapshotEvaluationStatus.INSUFFICIENT_EVIDENCE

    else:
        status = SnapshotEvaluationStatus.EVALUABLE

    return SnapshotEvaluationResult(
        snapshot_id=snapshot.snapshot_id,
        snapshot_version=snapshot.snapshot_version,
        case_id=snapshot.case_id,
        status=status,
        dimension_results=dimension_results,
    )
