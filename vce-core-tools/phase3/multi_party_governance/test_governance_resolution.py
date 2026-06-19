from phase3.multi_party_governance.governance_resolution import (
    GovernanceResolution,
)


def test_resolved_from_successful_quorum():

    resolution = GovernanceResolution.from_quorum(
        True
    )

    assert resolution.status == "RESOLVED"


def test_unresolved_from_failed_quorum():

    resolution = GovernanceResolution.from_quorum(
        False
    )

    assert resolution.status == "UNRESOLVED"


def test_resolution_serializes():

    resolution = GovernanceResolution.from_quorum(
        True
    )

    assert resolution.to_dict() == {
        "status": "RESOLVED"
    }
