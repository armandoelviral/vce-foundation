from phase3.governance_provenance.governance_provenance_record import (
    GovernanceProvenanceRecord,
)

from phase3.governance_provenance.lineage_evaluation import (
    LineageEvaluation,
)


def test_valid_lineage_passes():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    assert LineageEvaluation.evaluate(record) is True


def test_missing_current_snapshot_fails():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="",
        previous_snapshot="snap-001",
    )

    assert LineageEvaluation.evaluate(record) is False


def test_missing_previous_snapshot_fails():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="",
    )

    assert LineageEvaluation.evaluate(record) is False


def test_self_referential_lineage_fails():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-001",
        previous_snapshot="snap-001",
    )

    assert LineageEvaluation.evaluate(record) is False
