from phase4.trusted_compute_network_governance.governance_flow import (
    GovernanceFlow,
)


def test_generates_flow():

    result = GovernanceFlow.generate()

    assert "citizen_status" in result
    assert "governance_valid" in result


def test_citizen_active():

    result = GovernanceFlow.generate()

    assert (
        result["citizen_status"]
        == "ACTIVE"
    )


def test_governance_valid():

    result = GovernanceFlow.generate()

    assert (
        result["governance_valid"]
        is True
    )
