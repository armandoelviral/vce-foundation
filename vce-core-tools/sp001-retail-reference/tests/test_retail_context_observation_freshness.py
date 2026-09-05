from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_observation_freshness import (
    RetailContextObservationFreshnessEvaluation,
    RetailContextObservationFreshnessPolicy,
    RetailContextObservationFreshnessStatus,
    evaluate_retail_context_observation_freshness,
)
from sp001.contracts.retail_context_observation_provenance import (
    RetailContextObservationProvenance,
)
from sp001.contracts.retail_context_observation_provenance_binding import (
    bind_retail_context_observation_provenance,
)
from sp001.contracts.retail_context_snapshot import RetailContextSnapshot


OBSERVED_AT = datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc)


def create_binding(
    *,
    observed_at: datetime = OBSERVED_AT,
    recorded_at: datetime | None = None,
    effective_until: datetime | None = None,
):
    dimension = RetailContextDimension(
        dimension_id="DIMENSION-001",
        dimension_type="CUSTOMER_DEFINED_DIMENSION",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.MEASURED,
        value="OPAQUE-VALUE",
    )
    snapshot = RetailContextSnapshot(
        snapshot_id="SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=(dimension,),
    )
    provenance = RetailContextObservationProvenance(
        observation_id="OBSERVATION-001",
        observation_version=1,
        case_id="CASE-001",
        snapshot_id="SNAPSHOT-001",
        snapshot_version=1,
        dimension_id="DIMENSION-001",
        source_identity=KnowledgeSourceIdentity(
            source_id="SOURCE-001",
            source_version="v1",
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value="0" * 64,
            ),
        ),
        observed_at=observed_at,
        recorded_at=recorded_at or observed_at,
        effective_from=observed_at - timedelta(hours=1),
        effective_until=effective_until,
        evidence_ids=("EVIDENCE-001",),
    )
    return bind_retail_context_observation_provenance(
        snapshot=snapshot,
        provenance=provenance,
    )


def create_policy(
    *, maximum_age: timedelta = timedelta(hours=2)
) -> RetailContextObservationFreshnessPolicy:
    return RetailContextObservationFreshnessPolicy(
        freshness_policy_id="FRESHNESS-POLICY-001",
        freshness_policy_version=1,
        maximum_age=maximum_age,
    )


def evaluate(*, offset: timedelta):
    return evaluate_retail_context_observation_freshness(
        binding=create_binding(),
        policy=create_policy(),
        evaluated_at=OBSERVED_AT + offset,
    )


def test_freshness_status_vocabulary_is_exact() -> None:
    assert tuple(RetailContextObservationFreshnessStatus) == (
        RetailContextObservationFreshnessStatus.FRESH,
        RetailContextObservationFreshnessStatus.STALE,
        RetailContextObservationFreshnessStatus.NOT_YET_OBSERVED,
    )
    assert tuple(status.value for status in RetailContextObservationFreshnessStatus) == (
        "FRESH",
        "STALE",
        "NOT_YET_OBSERVED",
    )


def test_policy_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(RetailContextObservationFreshnessPolicy)) == (
        "freshness_policy_id",
        "freshness_policy_version",
        "maximum_age",
    )


def test_evaluation_fields_are_exact() -> None:
    assert tuple(
        field.name for field in fields(RetailContextObservationFreshnessEvaluation)
    ) == (
        "binding",
        "policy",
        "evaluated_at",
        "age",
        "freshness_status",
    )


@pytest.mark.parametrize("instance", (create_policy(), evaluate(offset=timedelta())))
def test_contracts_are_immutable(instance) -> None:
    with pytest.raises(FrozenInstanceError):
        instance.evaluated_at = OBSERVED_AT


@pytest.mark.parametrize("instance", (create_policy(), evaluate(offset=timedelta())))
def test_contracts_use_slots(instance) -> None:
    assert not hasattr(instance, "__dict__")


@pytest.mark.parametrize("value", (None, 1, object(), "   "))
def test_policy_id_must_be_nonempty_string(value) -> None:
    with pytest.raises(ValueError, match="freshness_policy_id must not be empty"):
        replace(create_policy(), freshness_policy_id=value)


@pytest.mark.parametrize("value", (None, True, False, 0, -1, 1.0, "1"))
def test_policy_version_must_be_strict_positive_integer(value) -> None:
    with pytest.raises(
        ValueError,
        match="freshness_policy_version must be a positive integer",
    ):
        replace(create_policy(), freshness_policy_version=value)


@pytest.mark.parametrize("value", (None, 1, 1.0, "PT1H", object()))
def test_maximum_age_requires_timedelta(value) -> None:
    with pytest.raises(TypeError, match="maximum_age must be a timedelta"):
        replace(create_policy(), maximum_age=value)


@pytest.mark.parametrize("value", (timedelta(), timedelta(microseconds=-1)))
def test_maximum_age_must_be_positive(value) -> None:
    with pytest.raises(ValueError, match="maximum_age must be positive"):
        replace(create_policy(), maximum_age=value)


def test_evaluation_at_observation_is_fresh_with_zero_age() -> None:
    result = evaluate(offset=timedelta())
    assert result.age == timedelta()
    assert result.freshness_status is RetailContextObservationFreshnessStatus.FRESH


def test_exact_maximum_age_is_fresh() -> None:
    result = evaluate(offset=timedelta(hours=2))
    assert result.age == timedelta(hours=2)
    assert result.freshness_status is RetailContextObservationFreshnessStatus.FRESH


def test_one_microsecond_over_maximum_age_is_stale() -> None:
    result = evaluate(offset=timedelta(hours=2, microseconds=1))
    assert result.age == timedelta(hours=2, microseconds=1)
    assert result.freshness_status is RetailContextObservationFreshnessStatus.STALE


def test_evaluation_before_observation_is_not_yet_observed() -> None:
    result = evaluate(offset=timedelta(microseconds=-1))
    assert result.age is None
    assert result.freshness_status is (
        RetailContextObservationFreshnessStatus.NOT_YET_OBSERVED
    )


def test_result_preserves_exact_binding_policy_and_instant() -> None:
    binding = create_binding()
    policy = create_policy()
    evaluated_at = OBSERVED_AT + timedelta(minutes=30)
    result = evaluate_retail_context_observation_freshness(
        binding=binding,
        policy=policy,
        evaluated_at=evaluated_at,
    )
    assert result.binding is binding
    assert result.policy is policy
    assert result.evaluated_at is evaluated_at


def test_age_uses_observed_at_not_recorded_at() -> None:
    binding = create_binding(recorded_at=OBSERVED_AT + timedelta(hours=12))
    result = evaluate_retail_context_observation_freshness(
        binding=binding,
        policy=create_policy(),
        evaluated_at=OBSERVED_AT + timedelta(hours=1),
    )
    assert result.age == timedelta(hours=1)
    assert result.freshness_status is RetailContextObservationFreshnessStatus.FRESH


def test_effective_until_does_not_become_a_freshness_validity_claim() -> None:
    binding = create_binding(effective_until=OBSERVED_AT + timedelta(minutes=15))
    result = evaluate_retail_context_observation_freshness(
        binding=binding,
        policy=create_policy(),
        evaluated_at=OBSERVED_AT + timedelta(hours=1),
    )
    assert result.freshness_status is RetailContextObservationFreshnessStatus.FRESH


def test_timezone_equivalent_instants_produce_zero_age() -> None:
    offset_zone = timezone(timedelta(hours=-6))
    result = evaluate_retail_context_observation_freshness(
        binding=create_binding(),
        policy=create_policy(),
        evaluated_at=OBSERVED_AT.astimezone(offset_zone),
    )
    assert result.age == timedelta()
    assert result.freshness_status is RetailContextObservationFreshnessStatus.FRESH


@pytest.mark.parametrize("binding", (None, "OBSERVATION-001", object()))
def test_evaluator_rejects_untyped_binding(binding) -> None:
    with pytest.raises(
        TypeError,
        match="binding must be a RetailContextObservationProvenanceBinding",
    ):
        evaluate_retail_context_observation_freshness(
            binding=binding,
            policy=create_policy(),
            evaluated_at=OBSERVED_AT,
        )


@pytest.mark.parametrize("policy", (None, "POLICY-001", object()))
def test_evaluator_rejects_untyped_policy(policy) -> None:
    with pytest.raises(
        TypeError,
        match="policy must be a RetailContextObservationFreshnessPolicy",
    ):
        evaluate_retail_context_observation_freshness(
            binding=create_binding(),
            policy=policy,
            evaluated_at=OBSERVED_AT,
        )


@pytest.mark.parametrize("value", (None, "2026-09-05T12:00:00Z", object()))
def test_evaluated_at_requires_datetime(value) -> None:
    with pytest.raises(TypeError, match="evaluated_at must be a datetime"):
        evaluate_retail_context_observation_freshness(
            binding=create_binding(),
            policy=create_policy(),
            evaluated_at=value,
        )


def test_evaluated_at_requires_timezone_awareness() -> None:
    with pytest.raises(ValueError, match="evaluated_at must be timezone-aware"):
        evaluate_retail_context_observation_freshness(
            binding=create_binding(),
            policy=create_policy(),
            evaluated_at=datetime(2026, 9, 5, 12, 0),
        )


def test_direct_evaluation_rejects_untyped_binding() -> None:
    with pytest.raises(
        TypeError,
        match="binding must be a RetailContextObservationProvenanceBinding",
    ):
        replace(evaluate(offset=timedelta()), binding=None)


def test_direct_evaluation_rejects_untyped_policy() -> None:
    with pytest.raises(
        TypeError,
        match="policy must be a RetailContextObservationFreshnessPolicy",
    ):
        replace(evaluate(offset=timedelta()), policy=None)


def test_future_evaluation_forbids_age() -> None:
    with pytest.raises(
        ValueError,
        match="NOT_YET_OBSERVED evaluation must not contain age",
    ):
        RetailContextObservationFreshnessEvaluation(
            binding=create_binding(),
            policy=create_policy(),
            evaluated_at=OBSERVED_AT - timedelta(seconds=1),
            age=timedelta(),
            freshness_status=RetailContextObservationFreshnessStatus.NOT_YET_OBSERVED,
        )


def test_future_evaluation_requires_not_yet_observed_status() -> None:
    with pytest.raises(ValueError, match="future observation requires NOT_YET_OBSERVED"):
        RetailContextObservationFreshnessEvaluation(
            binding=create_binding(),
            policy=create_policy(),
            evaluated_at=OBSERVED_AT - timedelta(seconds=1),
            age=None,
            freshness_status=RetailContextObservationFreshnessStatus.FRESH,
        )


@pytest.mark.parametrize("age", (None, 0, "PT0S"))
def test_completed_evaluation_requires_timedelta_age(age) -> None:
    with pytest.raises(
        TypeError,
        match="completed freshness evaluation requires timedelta age",
    ):
        replace(evaluate(offset=timedelta()), age=age)


def test_direct_evaluation_requires_exact_calculated_age() -> None:
    with pytest.raises(ValueError, match="age must equal evaluated_at minus observed_at"):
        replace(evaluate(offset=timedelta(hours=1)), age=timedelta(minutes=59))


@pytest.mark.parametrize(
    ("offset", "status"),
    (
        (timedelta(hours=1), RetailContextObservationFreshnessStatus.STALE),
        (timedelta(hours=3), RetailContextObservationFreshnessStatus.FRESH),
        (timedelta(), RetailContextObservationFreshnessStatus.NOT_YET_OBSERVED),
    ),
)
def test_direct_evaluation_requires_status_matching_policy(offset, status) -> None:
    with pytest.raises(
        ValueError,
        match="freshness_status must match policy age evaluation",
    ):
        replace(evaluate(offset=offset), freshness_status=status)


def test_direct_evaluation_rejects_untyped_status() -> None:
    with pytest.raises(
        TypeError,
        match="freshness_status must be a RetailContextObservationFreshnessStatus",
    ):
        replace(evaluate(offset=timedelta()), freshness_status="FRESH")


def test_evaluation_does_not_mutate_inputs() -> None:
    binding = create_binding()
    policy = create_policy()
    original_provenance = binding.provenance
    evaluate_retail_context_observation_freshness(
        binding=binding,
        policy=policy,
        evaluated_at=OBSERVED_AT + timedelta(hours=1),
    )
    assert binding.provenance is original_provenance
    assert policy.maximum_age == timedelta(hours=2)


def test_evaluator_requires_explicit_time_and_has_no_clock_read() -> None:
    signature = inspect.signature(evaluate_retail_context_observation_freshness)
    assert signature.parameters["evaluated_at"].default is inspect.Parameter.empty
    source = inspect.getsource(evaluate_retail_context_observation_freshness)
    assert "datetime.now" not in source
    assert "datetime.utcnow" not in source


def test_contract_adds_no_domain_authority_or_io_capability() -> None:
    source = inspect.getsource(
        __import__(
            "sp001.contracts.retail_context_observation_freshness",
            fromlist=["*"],
        )
    ).casefold()
    for forbidden in (
        "inventory",
        "sales",
        "visual",
        "human_capacity",
        "authentic",
        "authority",
        "accept",
        "open(",
        "read_",
        "write_",
        "requests",
    ):
        assert forbidden not in source
