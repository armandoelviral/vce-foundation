from phase3.governance_provenance.governance_provenance_record import (
    GovernanceProvenanceRecord,
)

from phase3.governance_provenance.provenance_registry import (
    ProvenanceRegistry,
)


def test_registry_starts_empty():

    registry = ProvenanceRegistry()

    assert registry.count() == 0


def test_registry_accepts_record():

    registry = ProvenanceRegistry()

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    registry.add(record)

    assert registry.count() == 1


def test_registry_returns_record():

    registry = ProvenanceRegistry()

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    registry.add(record)

    recovered = registry.get(
        "prov-001"
    )

    assert recovered == record


def test_missing_record_returns_none():

    registry = ProvenanceRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_provenance_ids():

    registry = ProvenanceRegistry()

    registry.add(
        GovernanceProvenanceRecord(
            provenance_id="prov-001",
            current_snapshot="snap-002",
            previous_snapshot="snap-001",
        )
    )

    registry.add(
        GovernanceProvenanceRecord(
            provenance_id="prov-002",
            current_snapshot="snap-003",
            previous_snapshot="snap-002",
        )
    )

    assert registry.provenance_ids() == [
        "prov-001",
        "prov-002",
    ]
