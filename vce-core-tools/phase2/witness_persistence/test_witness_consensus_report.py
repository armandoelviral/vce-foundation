from phase2.witness_persistence.consensus_decision_record import (
    ConsensusDecisionRecord,
)

from phase2.witness_persistence.witness_consensus_report import (
    WitnessConsensusReport,
)


def test_report_contains_total_decisions():

    records = [
        ConsensusDecisionRecord(
            decision_id="decision-001",
            approved=True,
            vote_count=3,
        ),
        ConsensusDecisionRecord(
            decision_id="decision-002",
            approved=False,
            vote_count=1,
        ),
    ]

    report = WitnessConsensusReport(records)

    assert report.total_decisions() == 2


def test_report_lists_decision_ids():

    records = [
        ConsensusDecisionRecord(
            decision_id="decision-001",
            approved=True,
            vote_count=3,
        ),
        ConsensusDecisionRecord(
            decision_id="decision-002",
            approved=False,
            vote_count=1,
        ),
    ]

    report = WitnessConsensusReport(records)

    assert report.decision_ids() == [
        "decision-001",
        "decision-002",
    ]


def test_report_serializes():

    records = [
        ConsensusDecisionRecord(
            decision_id="decision-001",
            approved=True,
            vote_count=3,
        )
    ]

    report = WitnessConsensusReport(records)

    assert report.to_dict() == {
        "total_decisions": 1,
        "decision_ids": [
            "decision-001",
        ],
    }
