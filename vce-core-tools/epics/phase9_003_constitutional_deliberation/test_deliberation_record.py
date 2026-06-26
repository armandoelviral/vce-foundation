from epics.phase9_003_constitutional_deliberation.deliberation_record import (
    DeliberationRecord,
)


def test_deliberation_record_creation():
    record = DeliberationRecord(
        deliberation_id="delib.001",
        proposal_id="proposal.001",
        participants=7,
    )

    assert record.deliberation_id == "delib.001"
    assert record.proposal_id == "proposal.001"


def test_requires_deliberation_id():
    try:
        DeliberationRecord(
            "",
            "proposal.001",
            7,
        )
        assert False
    except ValueError as exc:
        assert "deliberation_id" in str(exc)
