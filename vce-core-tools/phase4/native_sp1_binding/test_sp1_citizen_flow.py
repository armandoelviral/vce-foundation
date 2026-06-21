from phase4.native_sp1_binding.sp1_citizen_flow import (
    SP1CitizenFlow,
)


def test_generates_sp1_citizen_flow():

    result = SP1CitizenFlow.generate()

    assert "citizen_record" in result
    assert "claim" in result
    assert "trusted" in result


def test_claim_is_trusted():

    result = SP1CitizenFlow.generate()

    assert result["trusted"] is True


def test_claim_has_citizen():

    result = SP1CitizenFlow.generate()

    assert (
        result["claim"]["citizen_did"]
        == "did:tcn:test:01"
    )
