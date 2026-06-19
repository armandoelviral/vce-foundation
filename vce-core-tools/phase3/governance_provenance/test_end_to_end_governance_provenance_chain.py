from phase3.governance_provenance.governance_provenance_record import (
    GovernanceProvenanceRecord,
)

from phase3.governance_provenance.provenance_registry import (
    ProvenanceRegistry,
)

from phase3.governance_provenance.lineage_evaluation import (
    LineageEvaluation,
)

from phase3.governance_provenance.lineage_decision import (
    LineageDecision,
)

from phase3.governance_provenance.provenance_query import (
    ProvenanceQuery,
)

from phase3.governance_provenance.provenance_report import (
    ProvenanceReport,
)

from phase3.governance_provenance.provenance_attestation import (
    ProvenanceAttestation,
)


def test_end_to_end_governance_provenance_chain():

    registry = ProvenanceRegistry()

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    registry.add(record)

    evaluation = LineageEvaluation.evaluate(
        record
    )

    assert evaluation is True

    decision = LineageDecision.from_evaluation(
        evaluation
    )

    assert decision.status == "ACCEPT_LINEAGE"

    query = ProvenanceQuery(
        registry
    )

    recovered = query.by_id(
        "prov-001"
    )

    assert recovered == record

    report = ProvenanceReport(
        {
            "prov-001": recovered
        }
    )

    assert report.record_count() == 1
    assert report.provenance_ids() == [
        "prov-001",
    ]

    attestation = ProvenanceAttestation.attest(
        attestation_id="att-001",
        record=record,
    )

    assert attestation.subject == "governance_provenance"
    assert attestation.evidence_hash == "prov-001"
