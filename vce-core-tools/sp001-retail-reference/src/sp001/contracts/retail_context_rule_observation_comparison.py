from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_context_rule_observation import (
    RuleObservationStatus,
)
from sp001.contracts.retail_context_rule_observation_binding import (
    RuleObservationBinding,
)


class ObservationChangeStatus(StrEnum):
    """Observed change between two evaluations of the same rule."""

    IMPROVED = "IMPROVED"
    UNCHANGED = "UNCHANGED"
    REGRESSED = "REGRESSED"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class RuleObservationComparison:
    """Immutable comparison of initial and final retail observations."""

    rule_id: str
    rule_type: str
    snapshot_id: str
    snapshot_version: int
    case_id: str
    initial_observation_id: str
    final_observation_id: str
    initial_status: RuleObservationStatus
    final_status: RuleObservationStatus
    initial_evidence_ids: tuple[str, ...]
    final_evidence_ids: tuple[str, ...]
    change_status: ObservationChangeStatus


def compare_rule_observations(
    *,
    initial: RuleObservationBinding,
    final: RuleObservationBinding,
) -> RuleObservationComparison:
    """Compare two evidence-backed observations of the same rule."""

    if not isinstance(
        initial,
        RuleObservationBinding,
    ):
        raise TypeError(
            "initial must be a RuleObservationBinding"
        )

    if not isinstance(
        final,
        RuleObservationBinding,
    ):
        raise TypeError(
            "final must be a RuleObservationBinding"
        )

    identity_fields = (
        "rule_id",
        "snapshot_id",
        "snapshot_version",
        "case_id",
    )

    for field in identity_fields:
        if (
            getattr(initial, field)
            != getattr(final, field)
        ):
            raise ValueError(
                f"observation {field} does not match"
            )

    if (
        initial.observation_id
        == final.observation_id
    ):
        raise ValueError(
            "initial and final observations must be distinct"
        )

    conclusive_statuses = {
        RuleObservationStatus.CONFORMANT,
        RuleObservationStatus.NON_CONFORMANT,
    }

    if (
        initial.observation_status not in conclusive_statuses
        or final.observation_status not in conclusive_statuses
    ):
        change_status = (
            ObservationChangeStatus.INDETERMINATE
        )

    elif (
        initial.observation_status
        is RuleObservationStatus.NON_CONFORMANT
        and final.observation_status
        is RuleObservationStatus.CONFORMANT
    ):
        change_status = (
            ObservationChangeStatus.IMPROVED
        )

    elif (
        initial.observation_status
        is RuleObservationStatus.CONFORMANT
        and final.observation_status
        is RuleObservationStatus.NON_CONFORMANT
    ):
        change_status = (
            ObservationChangeStatus.REGRESSED
        )

    else:
        change_status = (
            ObservationChangeStatus.UNCHANGED
        )

    return RuleObservationComparison(
        rule_id=initial.rule_id,
        rule_type=initial.rule_type,
        snapshot_id=initial.snapshot_id,
        snapshot_version=initial.snapshot_version,
        case_id=initial.case_id,
        initial_observation_id=(
            initial.observation_id
        ),
        final_observation_id=(
            final.observation_id
        ),
        initial_status=(
            initial.observation_status
        ),
        final_status=(
            final.observation_status
        ),
        initial_evidence_ids=(
            initial.evidence_ids
        ),
        final_evidence_ids=(
            final.evidence_ids
        ),
        change_status=change_status,
    )
