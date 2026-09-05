from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone
import inspect

import pytest

from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeTemporalApplicabilityStatus,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_observation_provenance import (
    RetailContextObservationProvenance,
)
from sp001.contracts.retail_context_observation_provenance_binding import (
    RetailContextObservationProvenanceBinding,
    bind_retail_context_observation_provenance,
)
from sp001.contracts.retail_context_observation_temporal_applicability import (
    RetailContextObservationTemporalApplicabilityEvaluation,
    evaluate_retail_context_observation_temporal_applicability,
)
from sp001.contracts.retail_context_snapshot import RetailContextSnapshot


EFFECTIVE_FROM = datetime(2026, 9, 5, 11, 0, tzinfo=timezone.utc)
OBSERVED_AT = datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc)
EFFECTIVE_UNTIL = datetime(2026, 9, 5, 13, 0, tzinfo=timezone.utc)


def create_binding(
    *,
    observed_at: datetime = OBSERVED_AT,
    recorded_at: datetime | None = None,
    effective_from: datetime = EFFECTIVE_FROM,
    effective_until: datetime | None = EFFECTIVE_UNTIL,
) -> RetailContextObservationProvenanceBinding:
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
        effective_from=effective_from,
        effective_until=effective_until,
        evidence_ids=("EVIDENCE-001",),
    )
    return bind_retail_context_observation_provenance(
        snapshot=snapshot,
        provenance=provenance,
    )


def evaluate(
    *,
    evaluated_at: datetime,
    binding: RetailContextObservationProvenanceBinding | None = None,
) -> RetailContextObservationTemporalApplicabilityEvaluation:
    return evaluate_retail_context_observation_temporal_applicability(
        binding=binding or create_binding(),
        evaluated_at=evaluated_at,
    )


def test_evaluation_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            RetailContextObservationTemporalApplicabilityEvaluation,
        )
    ) == (
        "binding",
        "evaluated_at",
        "temporal_status",
    )


def test_evaluation_reuses_common_temporal_status_vocabulary() -> None:
    assert tuple(KnowledgeTemporalApplicabilityStatus) == (
        KnowledgeTemporalApplicabilityStatus.ACTIVE,
        KnowledgeTemporalApplicabilityStatus.NOT_YET_EFFECTIVE,
        KnowledgeTemporalApplicabilityStatus.EXPIRED,
    )


def test_evaluation_is_immutable() -> None:
    result = evaluate(evaluated_at=EFFECTIVE_FROM)
    with pytest.raises(FrozenInstanceError):
        result.temporal_status = KnowledgeTemporalApplicabilityStatus.EXPIRED


def test_evaluation_uses_slots() -> None:
    assert not hasattr(evaluate(evaluated_at=EFFECTIVE_FROM), "__dict__")


def test_result_preserves_exact_binding_and_evaluation_instant() -> None:
    binding = create_binding()
    evaluated_at = EFFECTIVE_FROM + timedelta(minutes=30)
    result = evaluate(binding=binding, evaluated_at=evaluated_at)
    assert result.binding is binding
    assert result.evaluated_at is evaluated_at


def test_one_microsecond_before_start_is_not_yet_effective() -> None:
    result = evaluate(evaluated_at=EFFECTIVE_FROM - timedelta(microseconds=1))
    assert result.temporal_status is (
        KnowledgeTemporalApplicabilityStatus.NOT_YET_EFFECTIVE
    )


def test_exact_start_is_active() -> None:
    result = evaluate(evaluated_at=EFFECTIVE_FROM)
    assert result.temporal_status is KnowledgeTemporalApplicabilityStatus.ACTIVE


def test_one_microsecond_before_end_is_active() -> None:
    result = evaluate(evaluated_at=EFFECTIVE_UNTIL - timedelta(microseconds=1))
    assert result.temporal_status is KnowledgeTemporalApplicabilityStatus.ACTIVE


def test_exact_end_is_expired() -> None:
    result = evaluate(evaluated_at=EFFECTIVE_UNTIL)
    assert result.temporal_status is KnowledgeTemporalApplicabilityStatus.EXPIRED


def test_after_end_is_expired() -> None:
    result = evaluate(evaluated_at=EFFECTIVE_UNTIL + timedelta(days=1))
    assert result.temporal_status is KnowledgeTemporalApplicabilityStatus.EXPIRED


def test_open_ended_interval_remains_active() -> None:
    binding = create_binding(effective_until=None)
    result = evaluate(
        binding=binding,
        evaluated_at=EFFECTIVE_FROM + timedelta(days=36500),
    )
    assert result.temporal_status is KnowledgeTemporalApplicabilityStatus.ACTIVE


def test_equivalent_timezone_instant_is_active_at_start() -> None:
    mexico_offset = timezone(timedelta(hours=-6))
    equivalent_start = EFFECTIVE_FROM.astimezone(mexico_offset)
    result = evaluate(evaluated_at=equivalent_start)
    assert result.temporal_status is KnowledgeTemporalApplicabilityStatus.ACTIVE


def test_applicability_uses_effective_from_not_observed_at() -> None:
    result = evaluate(evaluated_at=EFFECTIVE_FROM + timedelta(minutes=30))
    assert result.evaluated_at < result.binding.provenance.observed_at
    assert result.temporal_status is KnowledgeTemporalApplicabilityStatus.ACTIVE


def test_applicability_uses_effective_until_not_observation_age() -> None:
    observed_at = EFFECTIVE_UNTIL - timedelta(microseconds=1)
    binding = create_binding(observed_at=observed_at, recorded_at=observed_at)
    result = evaluate(binding=binding, evaluated_at=EFFECTIVE_UNTIL)
    assert result.evaluated_at - observed_at == timedelta(microseconds=1)
    assert result.temporal_status is KnowledgeTemporalApplicabilityStatus.EXPIRED


def test_recorded_at_does_not_change_applicability() -> None:
    binding = create_binding(recorded_at=OBSERVED_AT + timedelta(days=10))
    result = evaluate(binding=binding, evaluated_at=EFFECTIVE_FROM)
    assert result.temporal_status is KnowledgeTemporalApplicabilityStatus.ACTIVE


@pytest.mark.parametrize("binding", (None, "OBSERVATION-001", object()))
def test_evaluator_rejects_untyped_binding(binding) -> None:
    with pytest.raises(
        TypeError,
        match="binding must be a RetailContextObservationProvenanceBinding",
    ):
        evaluate_retail_context_observation_temporal_applicability(
            binding=binding,
            evaluated_at=EFFECTIVE_FROM,
        )


@pytest.mark.parametrize("value", (None, "2026-09-05T11:00:00Z", object()))
def test_evaluator_rejects_untyped_evaluated_at(value) -> None:
    with pytest.raises(TypeError, match="evaluated_at must be a datetime"):
        evaluate_retail_context_observation_temporal_applicability(
            binding=create_binding(),
            evaluated_at=value,
        )


def test_evaluator_rejects_naive_evaluated_at() -> None:
    with pytest.raises(ValueError, match="evaluated_at must be timezone-aware"):
        evaluate_retail_context_observation_temporal_applicability(
            binding=create_binding(),
            evaluated_at=datetime(2026, 9, 5, 11, 0),
        )


def test_direct_evaluation_rejects_untyped_binding() -> None:
    with pytest.raises(
        TypeError,
        match="binding must be a RetailContextObservationProvenanceBinding",
    ):
        replace(evaluate(evaluated_at=EFFECTIVE_FROM), binding=None)


@pytest.mark.parametrize("value", (None, "2026-09-05T11:00:00Z", object()))
def test_direct_evaluation_rejects_untyped_evaluated_at(value) -> None:
    with pytest.raises(TypeError, match="evaluated_at must be a datetime"):
        replace(evaluate(evaluated_at=EFFECTIVE_FROM), evaluated_at=value)


def test_direct_evaluation_rejects_naive_evaluated_at() -> None:
    with pytest.raises(ValueError, match="evaluated_at must be timezone-aware"):
        replace(
            evaluate(evaluated_at=EFFECTIVE_FROM),
            evaluated_at=datetime(2026, 9, 5, 11, 0),
        )


def test_direct_evaluation_rejects_untyped_status() -> None:
    with pytest.raises(
        TypeError,
        match="temporal_status must be a KnowledgeTemporalApplicabilityStatus",
    ):
        replace(evaluate(evaluated_at=EFFECTIVE_FROM), temporal_status="ACTIVE")


@pytest.mark.parametrize(
    ("evaluated_at", "incorrect_status"),
    (
        (
            EFFECTIVE_FROM - timedelta(microseconds=1),
            KnowledgeTemporalApplicabilityStatus.ACTIVE,
        ),
        (EFFECTIVE_FROM, KnowledgeTemporalApplicabilityStatus.NOT_YET_EFFECTIVE),
        (EFFECTIVE_UNTIL, KnowledgeTemporalApplicabilityStatus.ACTIVE),
    ),
)
def test_direct_evaluation_requires_status_matching_interval(
    evaluated_at: datetime,
    incorrect_status: KnowledgeTemporalApplicabilityStatus,
) -> None:
    valid = evaluate(evaluated_at=evaluated_at)
    with pytest.raises(
        ValueError,
        match="temporal_status must match effective interval evaluation",
    ):
        replace(valid, temporal_status=incorrect_status)


def test_evaluation_does_not_mutate_binding_or_provenance() -> None:
    binding = create_binding()
    provenance = binding.provenance
    evaluate(binding=binding, evaluated_at=EFFECTIVE_FROM)
    assert binding.provenance is provenance
    assert provenance.effective_from is EFFECTIVE_FROM
    assert provenance.effective_until is EFFECTIVE_UNTIL


def test_evaluator_requires_explicit_time_and_has_no_clock_read() -> None:
    signature = inspect.signature(
        evaluate_retail_context_observation_temporal_applicability
    )
    assert signature.parameters["evaluated_at"].default is inspect.Parameter.empty
    source = inspect.getsource(
        evaluate_retail_context_observation_temporal_applicability
    )
    assert "datetime.now" not in source
    assert "datetime.utcnow" not in source


def test_applicability_contract_has_no_freshness_dependency() -> None:
    module = __import__(
        "sp001.contracts.retail_context_observation_temporal_applicability",
        fromlist=["*"],
    )
    source = inspect.getsource(module)
    assert "observation_freshness" not in source
    assert "maximum_age" not in source
    assert "observed_at" not in source


def test_contract_adds_no_domain_authority_or_io_capability() -> None:
    module = __import__(
        "sp001.contracts.retail_context_observation_temporal_applicability",
        fromlist=["*"],
    )
    source = inspect.getsource(module).casefold()
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
