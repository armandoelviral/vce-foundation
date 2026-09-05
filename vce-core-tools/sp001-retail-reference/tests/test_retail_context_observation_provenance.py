from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.retail_context_observation_provenance import (
    RetailContextObservationProvenance,
)


OBSERVED_AT = datetime(
    2026,
    9,
    5,
    12,
    0,
    tzinfo=timezone.utc,
)

RECORDED_AT = OBSERVED_AT + timedelta(
    seconds=1,
)

EFFECTIVE_FROM = OBSERVED_AT - timedelta(
    minutes=5,
)

EFFECTIVE_UNTIL = OBSERVED_AT + timedelta(
    minutes=5,
)


def create_source_identity() -> KnowledgeSourceIdentity:
    return KnowledgeSourceIdentity(
        source_id="CONTEXT-SOURCE-001",
        source_version="v1",
        source_content_digest=KnowledgeContentDigest(
            algorithm="SHA-256",
            value="0" * 64,
        ),
    )


def create_provenance(
    **overrides: object,
) -> RetailContextObservationProvenance:
    values = {
        "observation_id": "CONTEXT-OBSERVATION-001",
        "observation_version": 1,
        "case_id": "CASE-001",
        "snapshot_id": "SNAPSHOT-001",
        "snapshot_version": 1,
        "dimension_id": "DIMENSION-001",
        "source_identity": create_source_identity(),
        "observed_at": OBSERVED_AT,
        "recorded_at": RECORDED_AT,
        "effective_from": EFFECTIVE_FROM,
        "evidence_ids": (
            "EVIDENCE-001",
        ),
        "effective_until": EFFECTIVE_UNTIL,
    }
    values.update(
        overrides,
    )

    return RetailContextObservationProvenance(
        **values,
    )


def test_provenance_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            RetailContextObservationProvenance,
        )
    ) == (
        "observation_id",
        "observation_version",
        "case_id",
        "snapshot_id",
        "snapshot_version",
        "dimension_id",
        "source_identity",
        "observed_at",
        "recorded_at",
        "effective_from",
        "evidence_ids",
        "effective_until",
    )


def test_provenance_is_immutable() -> None:
    provenance = create_provenance()

    with pytest.raises(
        FrozenInstanceError,
    ):
        provenance.dimension_id = "DIMENSION-002"


def test_provenance_uses_slots() -> None:
    assert not hasattr(
        create_provenance(),
        "__dict__",
    )


def test_provenance_preserves_context_identity() -> None:
    provenance = create_provenance()

    assert provenance.observation_id == (
        "CONTEXT-OBSERVATION-001"
    )
    assert provenance.observation_version == 1
    assert provenance.case_id == "CASE-001"
    assert provenance.snapshot_id == "SNAPSHOT-001"
    assert provenance.snapshot_version == 1
    assert provenance.dimension_id == "DIMENSION-001"


def test_provenance_preserves_exact_source_identity() -> None:
    source_identity = create_source_identity()

    provenance = create_provenance(
        source_identity=source_identity,
    )

    assert provenance.source_identity is source_identity


def test_provenance_preserves_all_temporal_facts() -> None:
    provenance = create_provenance()

    assert provenance.observed_at == OBSERVED_AT
    assert provenance.recorded_at == RECORDED_AT
    assert provenance.effective_from == EFFECTIVE_FROM
    assert provenance.effective_until == EFFECTIVE_UNTIL


def test_provenance_allows_recording_at_observation_time() -> None:
    provenance = create_provenance(
        recorded_at=OBSERVED_AT,
    )

    assert provenance.recorded_at == provenance.observed_at


def test_provenance_allows_observation_at_effective_start() -> None:
    provenance = create_provenance(
        effective_from=OBSERVED_AT,
    )

    assert provenance.observed_at == provenance.effective_from


def test_provenance_allows_open_effective_period() -> None:
    provenance = create_provenance(
        effective_until=None,
    )

    assert provenance.effective_until is None


def test_provenance_preserves_evidence_order() -> None:
    provenance = create_provenance(
        evidence_ids=(
            "EVIDENCE-003",
            "EVIDENCE-001",
            "EVIDENCE-002",
        ),
    )

    assert provenance.evidence_ids == (
        "EVIDENCE-003",
        "EVIDENCE-001",
        "EVIDENCE-002",
    )


@pytest.mark.parametrize(
    "field",
    (
        "observation_id",
        "case_id",
        "snapshot_id",
        "dimension_id",
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        "",
        "   ",
        None,
        1,
    ),
)
def test_provenance_rejects_invalid_identity(
    field: str,
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        create_provenance(
            **{
                field: value,
            },
        )


@pytest.mark.parametrize(
    "field",
    (
        "observation_version",
        "snapshot_version",
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        True,
        0,
        -1,
        1.0,
        "1",
        None,
    ),
)
def test_provenance_rejects_invalid_version(
    field: str,
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must be a positive integer",
    ):
        create_provenance(
            **{
                field: value,
            },
        )


def test_provenance_rejects_untyped_source_identity() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "source_identity must be a "
            "KnowledgeSourceIdentity"
        ),
    ):
        create_provenance(
            source_identity="CONTEXT-SOURCE-001",
        )


@pytest.mark.parametrize(
    "field",
    (
        "observed_at",
        "recorded_at",
        "effective_from",
        "effective_until",
    ),
)
def test_provenance_rejects_untyped_datetime(
    field: str,
) -> None:
    with pytest.raises(
        TypeError,
        match=f"{field} must be a datetime",
    ):
        create_provenance(
            **{
                field: "2026-09-05T12:00:00Z",
            },
        )


@pytest.mark.parametrize(
    "field",
    (
        "observed_at",
        "recorded_at",
        "effective_from",
        "effective_until",
    ),
)
def test_provenance_rejects_naive_datetime(
    field: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must be timezone-aware",
    ):
        create_provenance(
            **{
                field: datetime(
                    2026,
                    9,
                    5,
                    12,
                    0,
                ),
            },
        )


def test_provenance_rejects_recording_before_observation() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "recorded_at must not be before observed_at"
        ),
    ):
        create_provenance(
            recorded_at=(
                OBSERVED_AT
                - timedelta(
                    microseconds=1,
                )
            ),
        )


def test_provenance_rejects_observation_before_effective_start() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "observed_at must not be before effective_from"
        ),
    ):
        create_provenance(
            effective_from=(
                OBSERVED_AT
                + timedelta(
                    microseconds=1,
                )
            ),
        )


@pytest.mark.parametrize(
    "effective_until",
    (
        EFFECTIVE_FROM,
        EFFECTIVE_FROM - timedelta(
            microseconds=1,
        ),
    ),
)
def test_provenance_rejects_non_increasing_effective_period(
    effective_until: datetime,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "effective_until must be after effective_from"
        ),
    ):
        create_provenance(
            effective_until=effective_until,
        )


@pytest.mark.parametrize(
    "effective_until",
    (
        OBSERVED_AT,
        OBSERVED_AT - timedelta(
            microseconds=1,
        ),
    ),
)
def test_effective_period_end_is_exclusive(
    effective_until: datetime,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "observed_at must be before effective_until"
        ),
    ):
        create_provenance(
            effective_until=effective_until,
        )


def test_provenance_rejects_mutable_evidence_collection() -> None:
    with pytest.raises(
        TypeError,
        match="evidence_ids must be an immutable tuple",
    ):
        create_provenance(
            evidence_ids=[
                "EVIDENCE-001",
            ],
        )


def test_provenance_requires_evidence() -> None:
    with pytest.raises(
        ValueError,
        match="evidence_ids must not be empty",
    ):
        create_provenance(
            evidence_ids=(),
        )


@pytest.mark.parametrize(
    "evidence_id",
    (
        "",
        "   ",
        None,
        1,
    ),
)
def test_provenance_rejects_invalid_evidence_identity(
    evidence_id: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="evidence_id must not be empty",
    ):
        create_provenance(
            evidence_ids=(
                evidence_id,
            ),
        )


def test_provenance_rejects_duplicate_evidence_identity() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate evidence_id: EVIDENCE-001",
    ):
        create_provenance(
            evidence_ids=(
                "EVIDENCE-001",
                "EVIDENCE-001",
            ),
        )


def test_provenance_adds_no_domain_specific_semantics() -> None:
    field_names = {
        field.name
        for field in fields(
            RetailContextObservationProvenance,
        )
    }

    assert field_names.isdisjoint(
        {
            "sku",
            "stock",
            "sales",
            "margin",
            "image",
            "facing",
            "employee_count",
            "capacity",
        }
    )


def test_provenance_makes_no_freshness_authenticity_or_authority_claim() -> None:
    field_names = {
        field.name
        for field in fields(
            RetailContextObservationProvenance,
        )
    }

    assert field_names.isdisjoint(
        {
            "freshness_status",
            "is_fresh",
            "authenticity_status",
            "is_authentic",
            "authority_status",
            "is_authoritative",
            "acceptance_status",
            "is_accepted",
        }
    )
