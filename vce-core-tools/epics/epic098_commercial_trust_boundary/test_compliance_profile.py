from epics.epic098_commercial_trust_boundary.compliance_profile import (
    ComplianceProfile,
)


def test_contains_profile_id():

    profile = ComplianceProfile(
        profile_id="cnbv-fintech",
        jurisdiction="MX",
        residency_required=True,
        hsm_required=True,
    )

    assert profile.profile_id == "cnbv-fintech"


def test_contains_jurisdiction():

    profile = ComplianceProfile(
        profile_id="cnbv-fintech",
        jurisdiction="MX",
        residency_required=True,
        hsm_required=True,
    )

    assert profile.jurisdiction == "MX"


def test_requires_residency():

    profile = ComplianceProfile(
        profile_id="cnbv-fintech",
        jurisdiction="MX",
        residency_required=True,
        hsm_required=True,
    )

    assert profile.residency_required is True


def test_requires_hsm():

    profile = ComplianceProfile(
        profile_id="cnbv-fintech",
        jurisdiction="MX",
        residency_required=True,
        hsm_required=True,
    )

    assert profile.hsm_required is True


def test_serializes():

    profile = ComplianceProfile(
        profile_id="cnbv-fintech",
        jurisdiction="MX",
        residency_required=True,
        hsm_required=True,
    )

    assert profile.to_dict() == {
        "profile_id": "cnbv-fintech",
        "jurisdiction": "MX",
        "residency_required": True,
        "hsm_required": True,
    }
