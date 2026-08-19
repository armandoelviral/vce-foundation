from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_context_dimension_evaluation import (
    DimensionEvaluationStatus,
    evaluate_context_dimension,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


class ScopedEvaluationStatus(StrEnum):
    """Evaluation availability for a declared context dependency scope."""

    EVALUABLE = "EVALUABLE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    DISPUTED = "DISPUTED"


@dataclass(frozen=True, slots=True)
class ScopedEvaluationResult:
    """Immutable evaluation result for selected context dimensions."""

    snapshot_id: str
    snapshot_version: int
    case_id: str
    status: ScopedEvaluationStatus
    dimension_results: tuple[
        tuple[str, DimensionEvaluationStatus],
        ...,
    ]
    missing_dimension_ids: tuple[str, ...]


def evaluate_context_scope(
    snapshot: RetailContextSnapshot,
    *,
    required_dimension_ids: tuple[str, ...],
) -> ScopedEvaluationResult:
    """Evaluate only the dimensions required by a specific decision."""

    if not isinstance(
        snapshot,
        RetailContextSnapshot,
    ):
        raise TypeError(
            "snapshot must be a RetailContextSnapshot"
        )

    if not isinstance(
        required_dimension_ids,
        tuple,
    ):
        raise TypeError(
            "required_dimension_ids must be an immutable tuple"
        )

    if not required_dimension_ids:
        raise ValueError(
            "required_dimension_ids must not be empty"
        )

    seen_ids: set[str] = set()

    for dimension_id in required_dimension_ids:
        if (
            not isinstance(dimension_id, str)
            or not dimension_id.strip()
        ):
            raise ValueError(
                "required dimension_id must not be empty"
            )

        if dimension_id in seen_ids:
            raise ValueError(
                "duplicate required dimension_id: "
                f"{dimension_id}"
            )

        seen_ids.add(dimension_id)

    available_dimensions = {
        dimension.dimension_id: dimension
        for dimension in snapshot.dimensions
    }

    dimension_results = []
    missing_dimension_ids = []

    for dimension_id in required_dimension_ids:
        dimension = available_dimensions.get(
            dimension_id
        )

        if dimension is None:
            missing_dimension_ids.append(
                dimension_id
            )
            continue

        dimension_results.append(
            (
                dimension_id,
                evaluate_context_dimension(
                    dimension
                ),
            )
        )

    if any(
        result is DimensionEvaluationStatus.DISPUTED
        for _, result in dimension_results
    ):
        status = ScopedEvaluationStatus.DISPUTED

    elif missing_dimension_ids or any(
        result is not DimensionEvaluationStatus.EVALUABLE
        for _, result in dimension_results
    ):
        status = (
            ScopedEvaluationStatus.INSUFFICIENT_EVIDENCE
        )

    else:
        status = ScopedEvaluationStatus.EVALUABLE

    return ScopedEvaluationResult(
        snapshot_id=snapshot.snapshot_id,
        snapshot_version=snapshot.snapshot_version,
        case_id=snapshot.case_id,
        status=status,
        dimension_results=tuple(
            dimension_results
        ),
        missing_dimension_ids=tuple(
            missing_dimension_ids
        ),
    )
