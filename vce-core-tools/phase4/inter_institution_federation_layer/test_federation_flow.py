from phase4.inter_institution_federation_layer.federation_flow import (
    FederationFlow,
)


def test_generates_flow():

    result = FederationFlow.generate()

    assert "registry" in result
    assert "delegation" in result
    assert "trust" in result
    assert "treaty" in result
    assert "dispute" in result
    assert "state" in result


def test_trust_established():

    result = FederationFlow.generate()

    assert (
        result["trust"]["trusted"]
        is True
    )


def test_healthy_state():

    result = FederationFlow.generate()

    assert (
        result["state"]["federation_state"]
        == "HEALTHY"
    )
