from phase4.admission_policy_layer.admission_flow import (
    AdmissionFlow,
)


def test_generates_flow():

    result = AdmissionFlow.generate()

    assert "requirement" in result
    assert "policy" in result
    assert "state" in result
    assert "participation_allowed" in result


def test_admission_state():

    result = AdmissionFlow.generate()

    assert (
        result["state"]["admission_state"]
        == "ADMITTED"
    )


def test_participation_allowed():

    result = AdmissionFlow.generate()

    assert (
        result["participation_allowed"]
        is True
    )
