from phase4.policy_adjudication_layer.adjudication_flow import (
    AdjudicationFlow,
)


def test_generates_flow():

    result = AdjudicationFlow.generate()

    assert "conflict" in result
    assert "precedence" in result
    assert "appeal" in result
    assert "resolution" in result
    assert "state" in result
    assert "valid" in result


def test_resolution_is_upheld():

    result = AdjudicationFlow.generate()

    assert (
        result["resolution"]["resolution"]
        == "UPHELD"
    )


def test_adjudication_valid():

    result = AdjudicationFlow.generate()

    assert result["valid"] is True
