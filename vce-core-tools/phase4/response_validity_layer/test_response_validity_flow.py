from phase4.response_validity_layer.response_validity_flow import (
    ResponseValidityFlow,
)


def test_generates_flow():

    result = ResponseValidityFlow.generate()

    assert "capability" in result
    assert "state" in result
    assert "trusted" in result


def test_response_state():

    result = ResponseValidityFlow.generate()

    assert (
        result["state"]["response_state"]
        == "RECOVERED"
    )


def test_trust_preserved():

    result = ResponseValidityFlow.generate()

    assert result["trusted"] is True
