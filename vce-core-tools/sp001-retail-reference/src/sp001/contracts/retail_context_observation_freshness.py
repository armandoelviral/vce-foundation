from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from sp001.contracts.retail_context_observation_provenance_binding import (
    RetailContextObservationProvenanceBinding,
)


class RetailContextObservationFreshnessStatus(StrEnum):
    """Temporal freshness relative to one explicit evaluation instant."""

    FRESH = "FRESH"
    STALE = "STALE"
    NOT_YET_OBSERVED = "NOT_YET_OBSERVED"


@dataclass(frozen=True, slots=True)
class RetailContextObservationFreshnessPolicy:
    """Versioned maximum observation age without domain-specific meaning."""

    freshness_policy_id: str
    freshness_policy_version: int
    maximum_age: timedelta

    def __post_init__(self) -> None:
        if (
            not isinstance(
                self.freshness_policy_id,
                str,
            )
            or not self.freshness_policy_id.strip()
        ):
            raise ValueError(
                "freshness_policy_id must not be empty"
            )

        if (
            isinstance(
                self.freshness_policy_version,
                bool,
            )
            or not isinstance(
                self.freshness_policy_version,
                int,
            )
            or self.freshness_policy_version < 1
        ):
            raise ValueError(
                "freshness_policy_version must be a positive integer"
            )

        if not isinstance(
            self.maximum_age,
            timedelta,
        ):
            raise TypeError(
                "maximum_age must be a timedelta"
            )

        if self.maximum_age <= timedelta(0):
            raise ValueError(
                "maximum_age must be positive"
            )


@dataclass(frozen=True, slots=True)
class RetailContextObservationFreshnessEvaluation:
    """Reproducible observation-age evaluation without validity claims."""

    binding: RetailContextObservationProvenanceBinding
    policy: RetailContextObservationFreshnessPolicy
    evaluated_at: datetime
    age: timedelta | None
    freshness_status: RetailContextObservationFreshnessStatus

    def __post_init__(self) -> None:
        if not isinstance(
            self.binding,
            RetailContextObservationProvenanceBinding,
        ):
            raise TypeError(
                "binding must be a "
                "RetailContextObservationProvenanceBinding"
            )

        if not isinstance(
            self.policy,
            RetailContextObservationFreshnessPolicy,
        ):
            raise TypeError(
                "policy must be a "
                "RetailContextObservationFreshnessPolicy"
            )

        _validate_evaluated_at(
            self.evaluated_at,
        )

        if not isinstance(
            self.freshness_status,
            RetailContextObservationFreshnessStatus,
        ):
            raise TypeError(
                "freshness_status must be a "
                "RetailContextObservationFreshnessStatus"
            )

        observed_at = (
            self.binding.provenance.observed_at
        )

        if self.evaluated_at < observed_at:
            if self.age is not None:
                raise ValueError(
                    "NOT_YET_OBSERVED evaluation must not contain age"
                )

            if (
                self.freshness_status
                is not (
                    RetailContextObservationFreshnessStatus
                    .NOT_YET_OBSERVED
                )
            ):
                raise ValueError(
                    "future observation requires "
                    "NOT_YET_OBSERVED status"
                )

            return

        expected_age = self.evaluated_at - observed_at

        if not isinstance(
            self.age,
            timedelta,
        ):
            raise TypeError(
                "completed freshness evaluation requires timedelta age"
            )

        if self.age != expected_age:
            raise ValueError(
                "age must equal evaluated_at minus observed_at"
            )

        expected_status = (
            RetailContextObservationFreshnessStatus.FRESH
            if self.age <= self.policy.maximum_age
            else RetailContextObservationFreshnessStatus.STALE
        )

        if self.freshness_status is not expected_status:
            raise ValueError(
                "freshness_status must match policy age evaluation"
            )


def evaluate_retail_context_observation_freshness(
    *,
    binding: RetailContextObservationProvenanceBinding,
    policy: RetailContextObservationFreshnessPolicy,
    evaluated_at: datetime,
) -> RetailContextObservationFreshnessEvaluation:
    """Evaluate freshness from observed_at and an explicit maximum age."""

    if not isinstance(
        binding,
        RetailContextObservationProvenanceBinding,
    ):
        raise TypeError(
            "binding must be a "
            "RetailContextObservationProvenanceBinding"
        )

    if not isinstance(
        policy,
        RetailContextObservationFreshnessPolicy,
    ):
        raise TypeError(
            "policy must be a "
            "RetailContextObservationFreshnessPolicy"
        )

    _validate_evaluated_at(
        evaluated_at,
    )

    observed_at = binding.provenance.observed_at

    if evaluated_at < observed_at:
        age = None
        freshness_status = (
            RetailContextObservationFreshnessStatus
            .NOT_YET_OBSERVED
        )
    else:
        age = evaluated_at - observed_at
        freshness_status = (
            RetailContextObservationFreshnessStatus.FRESH
            if age <= policy.maximum_age
            else RetailContextObservationFreshnessStatus.STALE
        )

    return RetailContextObservationFreshnessEvaluation(
        binding=binding,
        policy=policy,
        evaluated_at=evaluated_at,
        age=age,
        freshness_status=freshness_status,
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
