from phase4.rights_permissions_layer.rights_flow import (
    RightsFlow,
)


def test_generates_flow():

    result = RightsFlow.generate()

    assert "permissions" in result
    assert "state" in result
    assert "authorized" in result


def test_rights_state():

    result = RightsFlow.generate()

    assert (
        result["state"]["rights_state"]
        == "ACTIVE"
    )


def test_authorized():

    result = RightsFlow.generate()

    assert result["authorized"] is True
