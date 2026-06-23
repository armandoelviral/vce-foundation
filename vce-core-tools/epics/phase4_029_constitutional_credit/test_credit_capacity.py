from epics.phase4_029_constitutional_credit.credit_capacity import (
    calculate_credit_capacity,
)


def test_credit_capacity_equals_available_capital():
    assert calculate_credit_capacity(100) == 100


def test_credit_capacity_for_zero_capital():
    assert calculate_credit_capacity(0) == 0


def test_rejects_negative_capital():
    try:
        calculate_credit_capacity(-1)
        assert False
    except ValueError as exc:
        assert "capital" in str(exc)
