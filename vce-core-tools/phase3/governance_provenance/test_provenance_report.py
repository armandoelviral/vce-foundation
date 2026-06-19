from phase3.governance_provenance.governance_provenance_record import (
    GovernanceProvenanceRecord,
)

from phase3.governance_provenance.provenance_report import (
    ProvenanceReport,
)


def test_report_contains_record_count():

    report = ProvenanceReport(
        {
            "prov-001":
                GovernanceProvenanceRecord(
                    provenance_id="prov-001",
                    current_snapshot="snap-002",
                    previous_snapshot="snap-001",
                )
        }
    )

    assert report.record_count() == 1


def test_report_lists_provenance_ids():

    report = ProvenanceReport(
        {
            "prov-001":
                GovernanceProvenanceRecord(
                    provenance_id="prov-001",
                    current_snapshot="snap-002",
                    previous_snapshot="snap-001",
                ),

            "prov-002":
                GovernanceProvenanceRecord(
                    provenance_id="prov-002",
                    current_snapshot="snap-003",
                    previous_snapshot="snap-002",
                ),
        }
    )

    assert report.provenance_ids() == [
        "prov-001",
        "prov-002",
    ]


def test_report_serializes():

    report = ProvenanceReport(
        {
            "prov-001":
                GovernanceProvenanceRecord(
                    provenance_id="prov-001",
                    current_snapshot="snap-002",
                    previous_snapshot="snap-001",
                )
        }
    )

    assert report.to_dict() == {
        "record_count": 1,
        "provenance_ids": [
            "prov-001",
        ],
    }
