from phase4.policy_enforcement_layer.policy_flow import (
    PolicyFlow,
)


def test_generates_flow():

    result = PolicyFlow.generate()

    assert "policy" in result
    assert "registry" in result
    assert "state" in result
    assert "valid" in result


def test_policy_active():

    result = PolicyFlow.generate()

    assert (
        result["policy"]["active"]
        is True
    )


def test_policy_valid():

    result = PolicyFlow.generate()

    assert (
        result["valid"]
        is True
    )
