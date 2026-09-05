from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timezone

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
from sp001.contracts.retail_context_observation_provenance import (
    RetailContextObservationProvenance,
)
from sp001.contracts.retail_context_observation_provenance_binding import (
    RetailContextObservationProvenanceBinding,
    bind_retail_context_observation_provenance,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


OBSERVED_AT = datetime(
    2026,
    9,
    5,
    12,
    0,
    tzinfo=timezone.utc,
)


def create_dimension(
    *,
    dimension_id: str = "DIMENSION-001",
    value: str = "OPAQUE-VALUE",
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type="CUSTOMER_DEFINED_DIMENSION",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.MEASURED,
        value=value,
    )


def create_snapshot(
    *dimensions: RetailContextDimension,
    snapshot_id: str = "SNAPSHOT-001",
    snapshot_version: int = 1,
    case_id: str = "CASE-001",
) -> RetailContextSnapshot:
    return RetailContextSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        case_id=case_id,
        dimensions=(
            dimensions
            if dimensions
            else (
                create_dimension(),
            )
        ),
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
        "recorded_at": OBSERVED_AT,
        "effective_from": OBSERVED_AT,
        "evidence_ids": (
            "EVIDENCE-001",
        ),
        "effective_until": None,
    }
    values.update(
        overrides,
    )

    return RetailContextObservationProvenance(
        **values,
    )


def create_binding() -> RetailContextObservationProvenanceBinding:
    dimension = create_dimension()
    snapshot = create_snapshot(
        dimension,
    )

    return bind_retail_context_observation_provenance(
        snapshot=snapshot,
        provenance=create_provenance(),
    )


def test_binding_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            RetailContextObservationProvenanceBinding,
        )
    ) == (
        "snapshot",
        "dimension",
        "provenance",
    )


def test_binding_is_immutable() -> None:
    binding = create_binding()

    with pytest.raises(
        FrozenInstanceError,
    ):
        binding.dimension = create_dimension(
            dimension_id="DIMENSION-002",
        )


def test_binding_uses_slots() -> None:
    assert not hasattr(
        create_binding(),
        "__dict__",
    )


def test_builder_preserves_exact_input_references() -> None:
    dimension = create_dimension()
    snapshot = create_snapshot(
        dimension,
    )
    provenance = create_provenance()

    binding = bind_retail_context_observation_provenance(
        snapshot=snapshot,
        provenance=provenance,
    )

    assert binding.snapshot is snapshot
    assert binding.dimension is dimension
    assert binding.provenance is provenance


def test_builder_selects_exact_declared_dimension() -> None:
    first = create_dimension(
        dimension_id="DIMENSION-001",
    )
    second = create_dimension(
        dimension_id="DIMENSION-002",
    )
    snapshot = create_snapshot(
        first,
        second,
    )

    binding = bind_retail_context_observation_provenance(
        snapshot=snapshot,
        provenance=create_provenance(
            dimension_id="DIMENSION-002",
        ),
    )

    assert binding.dimension is second


def test_binding_preserves_provenance_facts_without_projection() -> None:
    provenance = create_provenance(
        evidence_ids=(
            "EVIDENCE-002",
            "EVIDENCE-001",
        ),
    )
    dimension = create_dimension()

    binding = bind_retail_context_observation_provenance(
        snapshot=create_snapshot(
            dimension,
        ),
        provenance=provenance,
    )

    assert binding.provenance.source_identity is (
        provenance.source_identity
    )
    assert binding.provenance.observed_at is provenance.observed_at
    assert binding.provenance.evidence_ids is provenance.evidence_ids


@pytest.mark.parametrize(
    "snapshot",
    (
        None,
        "SNAPSHOT-001",
        object(),
    ),
)
def test_builder_rejects_untyped_snapshot(
    snapshot: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="snapshot must be a RetailContextSnapshot",
    ):
        bind_retail_context_observation_provenance(
            snapshot=snapshot,
            provenance=create_provenance(),
        )


@pytest.mark.parametrize(
    "provenance",
    (
        None,
        "CONTEXT-OBSERVATION-001",
        object(),
    ),
)
def test_builder_rejects_untyped_provenance(
    provenance: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "provenance must be a "
            "RetailContextObservationProvenance"
        ),
    ):
        bind_retail_context_observation_provenance(
            snapshot=create_snapshot(),
            provenance=provenance,
        )


@pytest.mark.parametrize(
    "field, value, message",
    (
        (
            "case_id",
            "CASE-002",
            "provenance case_id does not match snapshot",
        ),
        (
            "snapshot_id",
            "SNAPSHOT-002",
            "provenance snapshot_id does not match snapshot",
        ),
        (
            "snapshot_version",
            2,
            "provenance snapshot_version does not match snapshot",
        ),
    ),
)
def test_builder_rejects_snapshot_identity_mismatch(
    field: str,
    value: object,
    message: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=message,
    ):
        bind_retail_context_observation_provenance(
            snapshot=create_snapshot(),
            provenance=create_provenance(
                **{
                    field: value,
                },
            ),
        )


def test_builder_rejects_missing_dimension() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "provenance dimension_id not present in snapshot: "
            "DIMENSION-002"
        ),
    ):
        bind_retail_context_observation_provenance(
            snapshot=create_snapshot(),
            provenance=create_provenance(
                dimension_id="DIMENSION-002",
            ),
        )


@pytest.mark.parametrize(
    "field, value, message",
    (
        (
            "snapshot",
            None,
            "snapshot must be a RetailContextSnapshot",
        ),
        (
            "dimension",
            None,
            "dimension must be a RetailContextDimension",
        ),
        (
            "provenance",
            None,
            (
                "provenance must be a "
                "RetailContextObservationProvenance"
            ),
        ),
    ),
)
def test_direct_binding_rejects_untyped_members(
    field: str,
    value: object,
    message: str,
) -> None:
    dimension = create_dimension()
    values = {
        "snapshot": create_snapshot(
            dimension,
        ),
        "dimension": dimension,
        "provenance": create_provenance(),
    }
    values[field] = value

    with pytest.raises(
        TypeError,
        match=message,
    ):
        RetailContextObservationProvenanceBinding(
            **values,
        )


@pytest.mark.parametrize(
    "field, value, message",
    (
        (
            "case_id",
            "CASE-002",
            "provenance case_id does not match snapshot",
        ),
        (
            "snapshot_id",
            "SNAPSHOT-002",
            "provenance snapshot_id does not match snapshot",
        ),
        (
            "snapshot_version",
            2,
            "provenance snapshot_version does not match snapshot",
        ),
    ),
)
def test_direct_binding_rejects_snapshot_identity_mismatch(
    field: str,
    value: object,
    message: str,
) -> None:
    dimension = create_dimension()

    with pytest.raises(
        ValueError,
        match=message,
    ):
        RetailContextObservationProvenanceBinding(
            snapshot=create_snapshot(
                dimension,
            ),
            dimension=dimension,
            provenance=create_provenance(
                **{
                    field: value,
                },
            ),
        )


def test_direct_binding_rejects_dimension_identity_mismatch() -> None:
    dimension = create_dimension()

    with pytest.raises(
        ValueError,
        match=(
            "provenance dimension_id does not match dimension"
        ),
    ):
        RetailContextObservationProvenanceBinding(
            snapshot=create_snapshot(
                dimension,
            ),
            dimension=dimension,
            provenance=create_provenance(
                dimension_id="DIMENSION-002",
            ),
        )


def test_direct_binding_rejects_equal_foreign_dimension() -> None:
    declared_dimension = create_dimension()
    equal_foreign_dimension = replace(
        declared_dimension,
    )

    assert equal_foreign_dimension == declared_dimension
    assert equal_foreign_dimension is not declared_dimension

    with pytest.raises(
        ValueError,
        match="dimension must belong to snapshot",
    ):
        RetailContextObservationProvenanceBinding(
            snapshot=create_snapshot(
                declared_dimension,
            ),
            dimension=equal_foreign_dimension,
            provenance=create_provenance(),
        )


def test_builder_does_not_mutate_inputs() -> None:
    dimension = create_dimension()
    snapshot = create_snapshot(
        dimension,
    )
    provenance = create_provenance()
    original_dimensions = snapshot.dimensions
    original_evidence_ids = provenance.evidence_ids

    bind_retail_context_observation_provenance(
        snapshot=snapshot,
        provenance=provenance,
    )

    assert snapshot.dimensions is original_dimensions
    assert provenance.evidence_ids is original_evidence_ids


def test_binding_does_not_evaluate_dimension_value_or_status() -> None:
    dimension = RetailContextDimension(
        dimension_id="DIMENSION-001",
        dimension_type="OPAQUE",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="UNINTERPRETED",
    )

    binding = bind_retail_context_observation_provenance(
        snapshot=create_snapshot(
            dimension,
        ),
        provenance=create_provenance(),
    )

    assert binding.dimension is dimension


def test_binding_adds_no_freshness_authenticity_or_authority_result() -> None:
    field_names = {
        field.name
        for field in fields(
            RetailContextObservationProvenanceBinding,
        )
    }

    assert field_names == {
        "snapshot",
        "dimension",
        "provenance",
    }
