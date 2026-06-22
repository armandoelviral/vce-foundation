from phase4.policy_adjudication_layer.policy_precedence import (
    PolicyPrecedence,
)


def test_selects_higher_priority():

    result = PolicyPrecedence.resolve(
        higher_priority="policy-002",
        lower_priority="policy-001",
    )

    assert (
        result["winning_policy"]
        == "policy-002"
    )


def test_preserves_lower_priority():

    result = PolicyPrecedence.resolve(
        higher_priority="policy-002",
        lower_priority="policy-001",
    )

    assert (
        result["losing_policy"]
        == "policy-001"
    )


def test_serializes():

    result = PolicyPrecedence.resolve(
        higher_priority="policy-002",
        lower_priority="policy-001",
    )

    assert result == {
        "winning_policy":
            "policy-002",
        "losing_policy":
            "policy-001",
    }
