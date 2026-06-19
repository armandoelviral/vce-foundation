from phase3.trust_policy_engine.trust_decision import (
    TrustDecision,
)


def test_trusted_decision():

    decision = TrustDecision.from_evaluation(
        True
    )

    assert decision.status == "TRUSTED"


def test_untrusted_decision():

    decision = TrustDecision.from_evaluation(
        False
    )

    assert decision.status == "UNTRUSTED"


def test_decision_serializes():

    decision = TrustDecision.from_evaluation(
        True
    )

    assert decision.to_dict() == {
        "status": "TRUSTED"
    }
