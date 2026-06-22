from phase4.reputation_layer.reputation_flow import (
    ReputationFlow,
)


def test_generates_reputation_flow():

    result = ReputationFlow.generate()

    assert "events" in result
    assert "score" in result
    assert "state" in result
    assert "trusted" in result


def test_reputation_state():

    result = ReputationFlow.generate()

    assert result["state"]["reputation_state"] == "TRUSTED"


def test_trust_decision():

    result = ReputationFlow.generate()

    assert result["trusted"] is True
