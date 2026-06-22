from phase4.policy_adjudication_layer.exception_handling import (
    ExceptionHandling,
)


def test_grants_exception():

    result = ExceptionHandling.evaluate(
        policy_id="policy-001",
        exception_requested=True,
    )

    assert (
        result["exception_granted"]
        is True
    )


def test_denies_when_not_requested():

    result = ExceptionHandling.evaluate(
        policy_id="policy-001",
        exception_requested=False,
    )

    assert (
        result["exception_granted"]
        is False
    )


def test_serializes():

    result = ExceptionHandling.evaluate(
        policy_id="policy-001",
        exception_requested=True,
    )

    assert result == {
        "policy_id":
            "policy-001",
        "exception_granted":
            True,
    }
