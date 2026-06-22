from phase4.constitutional_evolution_layer.constitution_flow import (
    ConstitutionFlow,
)


def test_generates_flow():

    result = ConstitutionFlow.generate()

    assert "proposal" in result
    assert "amendment" in result
    assert "ratification" in result
    assert "version" in result
    assert "state" in result
    assert "history" in result
    assert "valid" in result


def test_constitution_valid():

    result = ConstitutionFlow.generate()

    assert result["valid"] is True


def test_latest_version():

    result = ConstitutionFlow.generate()

    assert (
        result["history"]["latest_version"]
        == "v2.0"
    )
