from epics.epic098_commercial_trust_boundary.jurisdiction_policy import (
    JurisdictionPolicy,
)


def test_contains_jurisdiction():

    policy = JurisdictionPolicy(
        jurisdiction="MX",
        allowed_regions=[
            "mx-central",
            "on-prem-bank",
        ],
    )

    assert policy.jurisdiction == "MX"


def test_contains_regions():

    policy = JurisdictionPolicy(
        jurisdiction="MX",
        allowed_regions=[
            "mx-central",
            "on-prem-bank",
        ],
    )

    assert len(policy.allowed_regions) == 2


def test_contains_region():

    policy = JurisdictionPolicy(
        jurisdiction="MX",
        allowed_regions=[
            "mx-central",
            "on-prem-bank",
        ],
    )

    assert "mx-central" in policy.allowed_regions


def test_serializes():

    policy = JurisdictionPolicy(
        jurisdiction="MX",
        allowed_regions=[
            "mx-central",
            "on-prem-bank",
        ],
    )

    assert policy.to_dict() == {
        "jurisdiction": "MX",
        "allowed_regions": [
            "mx-central",
            "on-prem-bank",
        ],
    }
