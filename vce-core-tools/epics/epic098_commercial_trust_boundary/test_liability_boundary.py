from epics.epic098_commercial_trust_boundary.liability_boundary import (
    LiabilityBoundary,
)


def test_contains_liability_cap():

    boundary = LiabilityBoundary(
        liability_cap=50000,
        consequential_damages_excluded=True,
        lost_profit_excluded=True,
    )

    assert boundary.liability_cap == 50000


def test_contains_consequential_clause():

    boundary = LiabilityBoundary(
        liability_cap=50000,
        consequential_damages_excluded=True,
        lost_profit_excluded=True,
    )

    assert boundary.consequential_damages_excluded is True


def test_contains_lost_profit_clause():

    boundary = LiabilityBoundary(
        liability_cap=50000,
        consequential_damages_excluded=True,
        lost_profit_excluded=True,
    )

    assert boundary.lost_profit_excluded is True


def test_serializes():

    boundary = LiabilityBoundary(
        liability_cap=50000,
        consequential_damages_excluded=True,
        lost_profit_excluded=True,
    )

    assert boundary.to_dict() == {
        "liability_cap": 50000,
        "consequential_damages_excluded": True,
        "lost_profit_excluded": True,
    }
