from phase4.constitutional_identity_layer.identity_flow import (
    IdentityFlow,
)


def test_generates_flow():

    result = IdentityFlow.generate()

    assert "right" in result
    assert "registry" in result
    assert "sovereignty" in result
    assert "revocation" in result
    assert "recovery" in result
    assert "continuity" in result
    assert "valid" in result


def test_identity_is_sovereign():

    result = IdentityFlow.generate()

    assert (
        result["sovereignty"]["sovereign"]
        is True
    )


def test_identity_valid():

    result = IdentityFlow.generate()

    assert result["valid"] is True
