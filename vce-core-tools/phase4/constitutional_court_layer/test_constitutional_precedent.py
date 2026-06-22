from phase4.constitutional_court_layer.constitutional_precedent import (
    ConstitutionalPrecedent,
)


def test_contains_case_id():

    precedent = ConstitutionalPrecedent(
        case_id="case-001",
        precedent="precedent-001",
    )

    assert precedent.case_id == (
        "case-001"
    )


def test_contains_precedent():

    precedent = ConstitutionalPrecedent(
        case_id="case-001",
        precedent="precedent-001",
    )

    assert precedent.precedent == (
        "precedent-001"
    )


def test_serializes():

    precedent = ConstitutionalPrecedent(
        case_id="case-001",
        precedent="precedent-001",
    )

    assert precedent.to_dict() == {
        "case_id":
            "case-001",
        "precedent":
            "precedent-001",
    }
