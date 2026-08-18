from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)
from sp001.models.case import Case


def test_snapshot_preserves_explicit_identity() -> None:
    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
    )

    assert snapshot.snapshot_id == "RCP-SNAPSHOT-001"
    assert snapshot.snapshot_version == 1


def test_snapshot_references_existing_case_identity() -> None:
    case = Case(
        case_id="CASE-001",
        objective_id="OBJ-001",
        objective_title="Verify retail fixture execution",
        scope="STORE-MX-001",
    )

    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id=case.case_id,
    )

    assert snapshot.case_id == case.case_id


def test_snapshot_is_immutable() -> None:
    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
    )

    with pytest.raises(FrozenInstanceError):
        snapshot.case_id = "CASE-002"


def test_distinct_versions_remain_distinct_snapshots() -> None:
    first = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
    )

    second = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=2,
        case_id="CASE-001",
    )

    assert first.snapshot_version == 1
    assert second.snapshot_version == 2
    assert first != second
