from phase4.constitutional_court_layer.constitutional_court_flow import (
    ConstitutionalCourtFlow,
)


def test_generates_flow():

    result = ConstitutionalCourtFlow.generate()

    assert "challenge" in result
    assert "review" in result
    assert "interpretation" in result
    assert "decision" in result
    assert "precedent" in result
    assert "state" in result
    assert "valid" in result


def test_decision_upheld():

    result = ConstitutionalCourtFlow.generate()

    assert (
        result["decision"]["decision"]
        == "UPHELD"
    )


def test_constitutional_validity():

    result = ConstitutionalCourtFlow.generate()

    assert result["valid"] is True
