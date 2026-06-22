from phase4.inter_institution_federation_layer.cross_institution_dispute import (
    CrossInstitutionDispute,
)


def test_contains_dispute_id():

    dispute = CrossInstitutionDispute(
        dispute_id="dispute-001",
        institution_a="inst-001",
        institution_b="inst-002",
        treaty_id="treaty-001",
    )

    assert dispute.dispute_id == (
        "dispute-001"
    )


def test_contains_institutions():

    dispute = CrossInstitutionDispute(
        dispute_id="dispute-001",
        institution_a="inst-001",
        institution_b="inst-002",
        treaty_id="treaty-001",
    )

    assert dispute.institution_a == "inst-001"
    assert dispute.institution_b == "inst-002"


def test_contains_treaty():

    dispute = CrossInstitutionDispute(
        dispute_id="dispute-001",
        institution_a="inst-001",
        institution_b="inst-002",
        treaty_id="treaty-001",
    )

    assert dispute.treaty_id == "treaty-001"


def test_serializes():

    dispute = CrossInstitutionDispute(
        dispute_id="dispute-001",
        institution_a="inst-001",
        institution_b="inst-002",
        treaty_id="treaty-001",
    )

    assert dispute.to_dict() == {
        "dispute_id":
            "dispute-001",
        "institution_a":
            "inst-001",
        "institution_b":
            "inst-002",
        "treaty_id":
            "treaty-001",
    }
