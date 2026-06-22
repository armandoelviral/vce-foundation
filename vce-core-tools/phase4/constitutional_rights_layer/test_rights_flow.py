from phase4.constitutional_rights_layer.rights_flow import (
    RightsFlow,
)


def test_generates_flow():

    result = RightsFlow.generate()

    assert "right" in result
    assert "registry" in result
    assert "protection" in result
    assert "violation" in result
    assert "appeal" in result
    assert "state" in result
    assert "valid" in result


def test_right_protected():

    result = RightsFlow.generate()

    assert (
        result["protection"]["protected"]
        is True
    )


def test_rights_valid():

    result = RightsFlow.generate()

    assert result["valid"] is True
