from phase3.governance_consensus_resolution.consensus_record import (
    ConsensusRecord,
)

from phase3.governance_consensus_resolution.consensus_report import (
    ConsensusReport,
)


def test_report_contains_consensus_count():

    report = ConsensusReport(
        {
            "consensus-001":
                ConsensusRecord(
                    consensus_id="consensus-001",
                    proposal_id="proposal-001",
                    outcome="APPROVED",
                )
        }
    )

    assert report.consensus_count() == 1


def test_report_lists_consensus_ids():

    report = ConsensusReport(
        {
            "consensus-001":
                ConsensusRecord(
                    consensus_id="consensus-001",
                    proposal_id="proposal-001",
                    outcome="APPROVED",
                ),

            "consensus-002":
                ConsensusRecord(
                    consensus_id="consensus-002",
                    proposal_id="proposal-002",
                    outcome="REJECTED",
                ),
        }
    )

    assert report.consensus_ids() == [
        "consensus-001",
        "consensus-002",
    ]


def test_report_serializes():

    report = ConsensusReport(
        {
            "consensus-001":
                ConsensusRecord(
                    consensus_id="consensus-001",
                    proposal_id="proposal-001",
                    outcome="APPROVED",
                )
        }
    )

    assert report.to_dict() == {
        "consensus_count": 1,
        "consensus_ids": [
            "consensus-001",
        ],
    }
