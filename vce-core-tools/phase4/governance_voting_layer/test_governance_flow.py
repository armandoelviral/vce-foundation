from phase4.governance_voting_layer.governance_flow import (
    GovernanceFlow,
)


def test_generates_flow():

    result = GovernanceFlow.generate()

    assert "proposal" in result
    assert "votes" in result
    assert "decision" in result
    assert "state" in result
    assert "valid" in result


def test_decision_approved():

    result = GovernanceFlow.generate()

    assert (
        result["decision"]["decision"]
        == "APPROVED"
    )


def test_governance_valid():

    result = GovernanceFlow.generate()

    assert result["valid"] is True
