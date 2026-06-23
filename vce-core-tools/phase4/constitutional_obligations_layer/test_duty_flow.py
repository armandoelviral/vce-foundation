from phase4.constitutional_obligations_layer.duty_flow import (
    DutyFlow,
)


def test_generates_flow():

    result = DutyFlow.generate()

    assert "duty" in result
    assert "registry" in result
    assert "compliance" in result
    assert "violation" in result
    assert "appeal" in result
    assert "state" in result
    assert "valid" in result


def test_duty_compliant():

    result = DutyFlow.generate()

    assert result["compliance"]["compliant"] is True


def test_duty_valid():

    result = DutyFlow.generate()

    assert result["valid"] is True
