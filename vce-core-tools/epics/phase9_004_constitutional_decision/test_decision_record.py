from epics.phase9_004_constitutional_decision.decision_record import (
    DecisionRecord,
)


def test_decision_record_creation():
    record = DecisionRecord(
        decision_id="decision.001",
        proposal_id="proposal.001",
        outcome="accepted",
    )

    assert record.decision_id == "decision.001"
    assert record.outcome == "accepted"


def test_requires_decision_id():
    try:
        DecisionRecord(
            "",
            "proposal.001",
            "accepted",
        )
        assert False
    except ValueError as exc:
        assert "decision_id" in str(exc)
