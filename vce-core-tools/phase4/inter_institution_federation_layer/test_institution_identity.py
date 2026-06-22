from phase4.inter_institution_federation_layer.institution_identity import (
    InstitutionIdentity,
)


def test_contains_institution_id():

    identity = InstitutionIdentity(
        institution_id="inst-001",
        institution_name="VCE Governance Council",
    )

    assert identity.institution_id == "inst-001"


def test_contains_institution_name():

    identity = InstitutionIdentity(
        institution_id="inst-001",
        institution_name="VCE Governance Council",
    )

    assert identity.institution_name == "VCE Governance Council"


def test_serializes():

    identity = InstitutionIdentity(
        institution_id="inst-001",
        institution_name="VCE Governance Council",
    )

    assert identity.to_dict() == {
        "institution_id": "inst-001",
        "institution_name": "VCE Governance Council",
    }
