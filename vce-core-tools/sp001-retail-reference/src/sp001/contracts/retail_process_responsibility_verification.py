from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from sp001.contracts.retail_process_responsibility_assignment import (
    RetailProcessResponsibilityAssignment,
)


class ResponsibilityCoverageStatus(StrEnum):
    """Structural participation coverage result."""

    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"


class ResponsibilitySegregationStatus(StrEnum):
    """Configured accountable-responsible separation result."""

    SATISFIED = "SATISFIED"
    VIOLATED = "VIOLATED"


class ResponsibilityEffectiveStatus(StrEnum):
    """Temporal applicability result for one explicit evaluation instant."""

    ACTIVE = "ACTIVE"
    NOT_YET_EFFECTIVE = "NOT_YET_EFFECTIVE"
    EXPIRED = "EXPIRED"


@dataclass(frozen=True, slots=True)
class RetailProcessResponsibilityVerificationPolicy:
    """Customer-scoped structural requirements for RACI verification."""

    verification_policy_id: str
    customer_id: str
    require_consulted: bool = False
    require_informed: bool = False
    require_accountable_responsible_separation: bool = True

    def __post_init__(self) -> None:
        identity_fields = {
            "verification_policy_id": (
                self.verification_policy_id
            ),
            "customer_id": self.customer_id,
        }

        for field, identity in identity_fields.items():
            if (
                not isinstance(
                    identity,
                    str,
                )
                or not identity.strip()
            ):
                raise ValueError(
                    f"{field} must not be empty"
                )

        boolean_fields = {
            "require_consulted": self.require_consulted,
            "require_informed": self.require_informed,
            "require_accountable_responsible_separation": (
                self.require_accountable_responsible_separation
            ),
        }

        for field, value in boolean_fields.items():
            if not isinstance(
                value,
                bool,
            ):
                raise TypeError(
                    f"{field} must be a boolean"
                )


@dataclass(frozen=True, slots=True)
class RetailProcessResponsibilityVerification:
    """Independent structural and temporal evaluation of one RACI assignment."""

    assignment: RetailProcessResponsibilityAssignment
    policy: RetailProcessResponsibilityVerificationPolicy
    evaluated_at: datetime
    coverage_status: ResponsibilityCoverageStatus
    missing_participation_types: tuple[str, ...]
    segregation_status: ResponsibilitySegregationStatus
    segregation_conflict_actor_ids: tuple[str, ...]
    effective_status: ResponsibilityEffectiveStatus

    def __post_init__(self) -> None:
        if not isinstance(
            self.assignment,
            RetailProcessResponsibilityAssignment,
        ):
            raise TypeError(
                "assignment must be a "
                "RetailProcessResponsibilityAssignment"
            )

        if not isinstance(
            self.policy,
            RetailProcessResponsibilityVerificationPolicy,
        ):
            raise TypeError(
                "policy must be a "
                "RetailProcessResponsibilityVerificationPolicy"
            )

        if (
            self.assignment.customer_id
            != self.policy.customer_id
        ):
            raise ValueError(
                "policy customer must match assignment customer"
            )

        _validate_evaluated_at(
            self.evaluated_at,
        )

        if not isinstance(
            self.coverage_status,
            ResponsibilityCoverageStatus,
        ):
            raise TypeError(
                "coverage_status must be a "
                "ResponsibilityCoverageStatus"
            )

        if not isinstance(
            self.segregation_status,
            ResponsibilitySegregationStatus,
        ):
            raise TypeError(
                "segregation_status must be a "
                "ResponsibilitySegregationStatus"
            )

        if not isinstance(
            self.effective_status,
            ResponsibilityEffectiveStatus,
        ):
            raise TypeError(
                "effective_status must be a "
                "ResponsibilityEffectiveStatus"
            )

        _validate_unique_string_tuple(
            field="missing_participation_types",
            values=self.missing_participation_types,
        )

        allowed_participation_types = {
            "RESPONSIBLE",
            "ACCOUNTABLE",
            "CONSULTED",
            "INFORMED",
        }

        for participation_type in (
            self.missing_participation_types
        ):
            if participation_type not in (
                allowed_participation_types
            ):
                raise ValueError(
                    "unknown missing participation_type: "
                    f"{participation_type}"
                )

        _validate_unique_string_tuple(
            field="segregation_conflict_actor_ids",
            values=self.segregation_conflict_actor_ids,
        )

        if (
            self.coverage_status
            is ResponsibilityCoverageStatus.COMPLETE
            and self.missing_participation_types
        ):
            raise ValueError(
                "COMPLETE coverage cannot contain "
                "missing participation types"
            )

        if (
            self.coverage_status
            is ResponsibilityCoverageStatus.INCOMPLETE
            and not self.missing_participation_types
        ):
            raise ValueError(
                "INCOMPLETE coverage requires "
                "missing participation types"
            )

        if (
            self.segregation_status
            is ResponsibilitySegregationStatus.SATISFIED
            and self.segregation_conflict_actor_ids
        ):
            raise ValueError(
                "SATISFIED segregation cannot contain "
                "conflict actor_ids"
            )

        if (
            self.segregation_status
            is ResponsibilitySegregationStatus.VIOLATED
            and not self.segregation_conflict_actor_ids
        ):
            raise ValueError(
                "VIOLATED segregation requires "
                "conflict actor_ids"
            )


def verify_retail_process_responsibility_assignment(
    *,
    assignment: RetailProcessResponsibilityAssignment,
    policy: RetailProcessResponsibilityVerificationPolicy,
    evaluated_at: datetime,
) -> RetailProcessResponsibilityVerification:
    """Evaluate coverage, configured segregation and temporal applicability."""

    if not isinstance(
        assignment,
        RetailProcessResponsibilityAssignment,
    ):
        raise TypeError(
            "assignment must be a "
            "RetailProcessResponsibilityAssignment"
        )

    if not isinstance(
        policy,
        RetailProcessResponsibilityVerificationPolicy,
    ):
        raise TypeError(
            "policy must be a "
            "RetailProcessResponsibilityVerificationPolicy"
        )

    if assignment.customer_id != policy.customer_id:
        raise ValueError(
            "policy customer must match assignment customer"
        )

    _validate_evaluated_at(
        evaluated_at,
    )

    missing_participation_types: list[str] = []

    if not assignment.responsible_actors:
        missing_participation_types.append(
            "RESPONSIBLE",
        )

    if assignment.accountable_actor is None:
        missing_participation_types.append(
            "ACCOUNTABLE",
        )

    if (
        policy.require_consulted
        and not assignment.consulted_actors
    ):
        missing_participation_types.append(
            "CONSULTED",
        )

    if (
        policy.require_informed
        and not assignment.informed_actors
    ):
        missing_participation_types.append(
            "INFORMED",
        )

    if missing_participation_types:
        coverage_status = (
            ResponsibilityCoverageStatus.INCOMPLETE
        )
    else:
        coverage_status = (
            ResponsibilityCoverageStatus.COMPLETE
        )

    segregation_conflict_actor_ids: list[str] = []

    if (
        policy.require_accountable_responsible_separation
    ):
        responsible_actor_ids = {
            actor.actor_id
            for actor in assignment.responsible_actors
        }

        if (
            assignment.accountable_actor.actor_id
            in responsible_actor_ids
        ):
            segregation_conflict_actor_ids.append(
                assignment.accountable_actor.actor_id,
            )

    if segregation_conflict_actor_ids:
        segregation_status = (
            ResponsibilitySegregationStatus.VIOLATED
        )
    else:
        segregation_status = (
            ResponsibilitySegregationStatus.SATISFIED
        )

    if evaluated_at < assignment.effective_from:
        effective_status = (
            ResponsibilityEffectiveStatus.NOT_YET_EFFECTIVE
        )
    elif (
        assignment.effective_until is not None
        and evaluated_at >= assignment.effective_until
    ):
        effective_status = (
            ResponsibilityEffectiveStatus.EXPIRED
        )
    else:
        effective_status = (
            ResponsibilityEffectiveStatus.ACTIVE
        )

    return RetailProcessResponsibilityVerification(
        assignment=assignment,
        policy=policy,
        evaluated_at=evaluated_at,
        coverage_status=coverage_status,
        missing_participation_types=tuple(
            missing_participation_types,
        ),
        segregation_status=segregation_status,
        segregation_conflict_actor_ids=tuple(
            segregation_conflict_actor_ids,
        ),
        effective_status=effective_status,
    )


def _validate_evaluated_at(
    value: object,
) -> None:
    if not isinstance(
        value,
        datetime,
    ):
        raise TypeError(
            "evaluated_at must be a datetime"
        )

    if (
        value.tzinfo is None
        or value.utcoffset() is None
    ):
        raise ValueError(
            "evaluated_at must be timezone-aware"
        )


def _validate_unique_string_tuple(
    *,
    field: str,
    values: object,
) -> None:
    if not isinstance(
        values,
        tuple,
    ):
        raise TypeError(
            f"{field} must be an immutable tuple"
        )

    seen_values: set[str] = set()

    for value in values:
        if (
            not isinstance(
                value,
                str,
            )
            or not value.strip()
        ):
            raise ValueError(
                f"{field} values must not be empty"
            )

        if value in seen_values:
            raise ValueError(
                f"duplicate {field} value: {value}"
            )

        seen_values.add(
            value,
        )
