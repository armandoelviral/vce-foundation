from phase3.governance_provenance.governance_provenance_record import (
    GovernanceProvenanceRecord,
)

from phase3.governance_provenance.provenance_registry import (
    ProvenanceRegistry,
)

from phase3.governance_provenance.provenance_query import (
    ProvenanceQuery,
)


def test_query_returns_record():

    registry = ProvenanceRegistry()

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    registry.add(record)

    query = ProvenanceQuery(
        registry
    )

    result = query.by_id(
        "prov-001"
    )

    assert result == record


def test_query_returns_none_for_missing():

    registry = ProvenanceRegistry()

    query = ProvenanceQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_current_snapshot():

    registry = ProvenanceRegistry()

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    registry.add(record)

    query = ProvenanceQuery(
        registry
    )

    result = query.by_id(
        "prov-001"
    )

    assert (
        result.current_snapshot
        == "snap-002"
    )
