from phase4.inter_institution_federation_layer.treaty_record import (
    TreatyRecord,
)


def test_contains_treaty_id():

    treaty = TreatyRecord(
        treaty_id="treaty-001",
        institution_a="inst-001",
        institution_b="inst-002",
        treaty_type="mutual_adjudication",
    )

    assert treaty.treaty_id == "treaty-001"


def test_contains_participants():

    treaty = TreatyRecord(
        treaty_id="treaty-001",
        institution_a="inst-001",
        institution_b="inst-002",
        treaty_type="mutual_adjudication",
    )

    assert treaty.institution_a == "inst-001"
    assert treaty.institution_b == "inst-002"


def test_contains_treaty_type():

    treaty = TreatyRecord(
        treaty_id="treaty-001",
        institution_a="inst-001",
        institution_b="inst-002",
        treaty_type="mutual_adjudication",
    )

    assert treaty.treaty_type == (
        "mutual_adjudication"
    )


def test_serializes():

    treaty = TreatyRecord(
        treaty_id="treaty-001",
        institution_a="inst-001",
        institution_b="inst-002",
        treaty_type="mutual_adjudication",
    )

    assert treaty.to_dict() == {
        "treaty_id":
            "treaty-001",
        "institution_a":
            "inst-001",
        "institution_b":
            "inst-002",
        "treaty_type":
            "mutual_adjudication",
    }
