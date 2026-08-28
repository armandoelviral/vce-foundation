from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
    KnowledgeSourceTemporalEvaluation,
    KnowledgeTemporalApplicabilityStatus,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)
from sp001.contracts.knowledge_source_status import (
    KnowledgeEvidenceStatus,
    KnowledgeLifecycleStatus,
    KnowledgeSourceStatus,
)
from sp001.services.knowledge_source_temporal_applicability import (
    evaluate_knowledge_source_temporal_applicability,
)


EFFECTIVE_FROM = datetime(
    2026,
    3,
    1,
    tzinfo=timezone.utc,
)

EFFECTIVE_UNTIL = datetime(
    2026,
    6,
    1,
    tzinfo=timezone.utc,
)


def create_source_status() -> KnowledgeSourceStatus:
    return KnowledgeSourceStatus(
        status_record_id="KG-STATUS-001",
        status_version=1,
        identity=KnowledgeSourceIdentity(
            source_id="POG-2026-DENIM-012",
            source_version="v1.0",
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value="0" * 64,
            ),
        ),
        scope=KnowledgeSourceScope(
            organization_id="RETAIL-GROUP-GLOBAL",
            customer_id="BRAND-CASUAL-X",
            jurisdiction="MX",
            commercial_channel_id="PHYSICAL_STORE",
            document_type=KnowledgeDocumentType.PLANOGRAM,
            point_of_sale_scope=KnowledgeScopeSelection(
                mode=KnowledgeScopeMode.EXPLICIT,
                ids=(
                    "POS-045",
                ),
            ),
            department_scope=KnowledgeScopeSelection(
                mode=KnowledgeScopeMode.EXPLICIT,
                ids=(
                    "DPT-DENIM",
                ),
            ),
            campaign_id="CAMP-SPRING-2026",
        ),
        lifecycle_status=KnowledgeLifecycleStatus.APPROVED,
        evidence_status=KnowledgeEvidenceStatus.SUPPORTED,
    )


def create_period(
    *,
    effective_from: datetime = EFFECTIVE_FROM,
    effective_until: datetime | None = EFFECTIVE_UNTIL,
) -> KnowledgeSourceEffectivePeriod:
    return KnowledgeSourceEffectivePeriod(
        source_status=create_source_status(),
        effective_from=effective_from,
        effective_until=effective_until,
    )


def evaluate(
    *,
    period: KnowledgeSourceEffectivePeriod | None = None,
    evaluated_at: datetime = EFFECTIVE_FROM,
) -> KnowledgeSourceTemporalEvaluation:
    return evaluate_knowledge_source_temporal_applicability(
        effective_period=(
            period
            if period is not None
            else create_period()
        ),
        evaluated_at=evaluated_at,
    )


def test_temporal_status_vocabulary_is_exact() -> None:
    assert tuple(
        KnowledgeTemporalApplicabilityStatus
    ) == (
        KnowledgeTemporalApplicabilityStatus.ACTIVE,
        KnowledgeTemporalApplicabilityStatus.NOT_YET_EFFECTIVE,
        KnowledgeTemporalApplicabilityStatus.EXPIRED,
    )


def test_effective_period_preserves_source_status_and_interval() -> None:
    source_status = create_source_status()

    period = KnowledgeSourceEffectivePeriod(
        source_status=source_status,
        effective_from=EFFECTIVE_FROM,
        effective_until=EFFECTIVE_UNTIL,
    )

    assert period.source_status is source_status
    assert period.effective_from == EFFECTIVE_FROM
    assert period.effective_until == EFFECTIVE_UNTIL


def test_effective_period_is_immutable() -> None:
    period = create_period()

    with pytest.raises(FrozenInstanceError):
        period.effective_until = None


def test_effective_period_rejects_untyped_source_status() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "source_status must be a "
            "KnowledgeSourceStatus"
        ),
    ):
        KnowledgeSourceEffectivePeriod(
            source_status="KG-STATUS-001",
            effective_from=EFFECTIVE_FROM,
        )


@pytest.mark.parametrize(
    "field",
    (
        "effective_from",
        "effective_until",
    ),
)
def test_effective_period_rejects_untyped_datetime(
    field: str,
) -> None:
    values = {
        "effective_from": EFFECTIVE_FROM,
        "effective_until": EFFECTIVE_UNTIL,
    }
    values[field] = "2026-03-01T00:00:00Z"

    with pytest.raises(
        TypeError,
        match=f"{field} must be a datetime",
    ):
        create_period(
            effective_from=values["effective_from"],
            effective_until=values["effective_until"],
        )


@pytest.mark.parametrize(
    "field",
    (
        "effective_from",
        "effective_until",
    ),
)
def test_effective_period_rejects_naive_datetime(
    field: str,
) -> None:
    values = {
        "effective_from": EFFECTIVE_FROM,
        "effective_until": EFFECTIVE_UNTIL,
    }
    values[field] = datetime(
        2026,
        3,
        1,
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must be timezone-aware",
    ):
        create_period(
            effective_from=values["effective_from"],
            effective_until=values["effective_until"],
        )


@pytest.mark.parametrize(
    "effective_until",
    (
        EFFECTIVE_FROM,
        EFFECTIVE_FROM - timedelta(seconds=1),
    ),
)
def test_effective_period_rejects_non_increasing_end(
    effective_until: datetime,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "effective_until must be "
            "after effective_from"
        ),
    ):
        create_period(
            effective_until=effective_until,
        )


def test_open_ended_effective_period_is_allowed() -> None:
    period = create_period(
        effective_until=None,
    )

    assert period.effective_until is None


def test_source_is_not_yet_effective_before_start() -> None:
    result = evaluate(
        evaluated_at=(
            EFFECTIVE_FROM
            - timedelta(
                microseconds=1,
            )
        ),
    )

    assert result.temporal_status is (
        KnowledgeTemporalApplicabilityStatus.NOT_YET_EFFECTIVE
    )


def test_source_is_active_exactly_at_start() -> None:
    result = evaluate(
        evaluated_at=EFFECTIVE_FROM,
    )

    assert result.temporal_status is (
        KnowledgeTemporalApplicabilityStatus.ACTIVE
    )


def test_source_is_active_before_exclusive_end() -> None:
    result = evaluate(
        evaluated_at=(
            EFFECTIVE_UNTIL
            - timedelta(
                microseconds=1,
            )
        ),
    )

    assert result.temporal_status is (
        KnowledgeTemporalApplicabilityStatus.ACTIVE
    )


def test_source_is_expired_exactly_at_exclusive_end() -> None:
    result = evaluate(
        evaluated_at=EFFECTIVE_UNTIL,
    )

    assert result.temporal_status is (
        KnowledgeTemporalApplicabilityStatus.EXPIRED
    )


def test_open_ended_source_remains_active() -> None:
    period = create_period(
        effective_until=None,
    )

    result = evaluate(
        period=period,
        evaluated_at=(
            EFFECTIVE_FROM
            + timedelta(
                days=3650,
            )
        ),
    )

    assert result.temporal_status is (
        KnowledgeTemporalApplicabilityStatus.ACTIVE
    )


def test_evaluation_accepts_equivalent_timezone_instant() -> None:
    mexico_offset = timezone(
        timedelta(
            hours=-6,
        )
    )
    equivalent_start = datetime(
        2026,
        2,
        28,
        18,
        0,
        tzinfo=mexico_offset,
    )

    result = evaluate(
        evaluated_at=equivalent_start,
    )

    assert result.temporal_status is (
        KnowledgeTemporalApplicabilityStatus.ACTIVE
    )


def test_evaluation_preserves_explicit_evaluation_instant() -> None:
    evaluated_at = datetime(
        2026,
        4,
        15,
        12,
        30,
        tzinfo=timezone.utc,
    )

    result = evaluate(
        evaluated_at=evaluated_at,
    )

    assert result.evaluated_at is evaluated_at


def test_evaluation_rejects_untyped_period() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "effective_period must be a "
            "KnowledgeSourceEffectivePeriod"
        ),
    ):
        evaluate_knowledge_source_temporal_applicability(
            effective_period="KG-PERIOD-001",
            evaluated_at=EFFECTIVE_FROM,
        )


def test_evaluation_rejects_untyped_instant() -> None:
    with pytest.raises(
        TypeError,
        match="evaluated_at must be a datetime",
    ):
        evaluate(
            evaluated_at="2026-03-01T00:00:00Z",
        )


def test_evaluation_rejects_naive_instant() -> None:
    with pytest.raises(
        ValueError,
        match="evaluated_at must be timezone-aware",
    ):
        evaluate(
            evaluated_at=datetime(
                2026,
                3,
                1,
            ),
        )


def test_temporal_evaluation_does_not_mutate_source_status() -> None:
    period = create_period()
    original_lifecycle = (
        period.source_status.lifecycle_status
    )
    original_evidence = (
        period.source_status.evidence_status
    )

    evaluate(
        period=period,
    )

    assert (
        period.source_status.lifecycle_status
        is original_lifecycle
    )
    assert (
        period.source_status.evidence_status
        is original_evidence
    )


def test_temporal_evaluation_does_not_claim_retrieval_or_authority() -> None:
    result = evaluate()

    for attribute in (
        "valid",
        "retrieval_eligible",
        "applicable",
        "authority_status",
        "authority_verified",
        "approved",
        "compliance_status",
        "commercial_outcome",
    ):
        assert not hasattr(
            result,
            attribute,
        )
