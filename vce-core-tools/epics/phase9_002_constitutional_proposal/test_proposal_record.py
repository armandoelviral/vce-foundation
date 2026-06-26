from epics.phase9_002_constitutional_proposal.proposal_record import (
    ProposalRecord,
)


def test_proposal_record_creation():
    proposal = ProposalRecord(
        proposal_id="proposal.001",
        intent_id="intent.001",
        title="Preserve Historical Evidence",
    )

    assert proposal.proposal_id == "proposal.001"
    assert proposal.intent_id == "intent.001"


def test_requires_proposal_id():
    try:
        ProposalRecord(
            "",
            "intent.001",
            "Title",
        )
        assert False
    except ValueError as exc:
        assert "proposal_id" in str(exc)
