from phase3.governance_provenance.governance_provenance_record import (
    GovernanceProvenanceRecord,
)


def test_contains_provenance_id():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    assert (
        record.provenance_id
        == "prov-001"
    )


def test_contains_current_snapshot():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    assert (
        record.current_snapshot
        == "snap-002"
    )


def test_contains_previous_snapshot():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    assert (
        record.previous_snapshot
        == "snap-001"
    )


def test_serializes():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    assert record.to_dict() == {
        "provenance_id": "prov-001",
        "current_snapshot": "snap-002",
        "previous_snapshot": "snap-001",
    }
