from phase4.reputation_constitution_layer.reputation_flow import (
    ReputationFlow,
)


def test_generates_flow():

    result = ReputationFlow.generate()

    assert "claim" in result
    assert "evidence" in result
    assert "accrual" in result
    assert "loss" in result
    assert "appeal" in result
    assert "state" in result
    assert "valid" in result


def test_positive_reputation():

    result = ReputationFlow.generate()

    assert (
        result["state"]["score"]
        == 95
    )


def test_valid_reputation():

    result = ReputationFlow.generate()

    assert result["valid"] is True
