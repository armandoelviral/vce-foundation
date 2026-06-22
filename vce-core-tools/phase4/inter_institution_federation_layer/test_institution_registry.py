from phase4.inter_institution_federation_layer.institution_registry import (
    InstitutionRegistry,
)

from phase4.inter_institution_federation_layer.institution_identity import (
    InstitutionIdentity,
)


def test_contains_institutions():

    registry = InstitutionRegistry(
        institutions=[
            InstitutionIdentity(
                institution_id="inst-001",
                institution_name="VCE Governance Council",
            ),
        ]
    )

    assert len(registry.institutions) == 1


def test_contains_institution_id():

    registry = InstitutionRegistry(
        institutions=[
            InstitutionIdentity(
                institution_id="inst-001",
                institution_name="VCE Governance Council",
            ),
        ]
    )

    assert (
        registry.institutions[0].institution_id
        == "inst-001"
    )


def test_serializes():

    registry = InstitutionRegistry(
        institutions=[
            InstitutionIdentity(
                institution_id="inst-001",
                institution_name="VCE Governance Council",
            ),
        ]
    )

    assert registry.to_dict() == {
        "institutions": [
            {
                "institution_id":
                    "inst-001",
                "institution_name":
                    "VCE Governance Council",
            }
        ]
    }
