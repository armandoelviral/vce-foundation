from epics.phase9_002_constitutional_proposal.proposal_builder import (
    proposal_built,
)


def test_valid_proposal():
    assert proposal_built(
        title="Preserve Historical Evidence"
    ) is True


def test_invalid_proposal():
    assert proposal_built(title="") is False
