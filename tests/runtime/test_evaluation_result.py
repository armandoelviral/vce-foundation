import pytest

from has.runtime.evaluation_result import EvaluationResult


def test_eligible_result_has_no_reasons() -> None:
    result = EvaluationResult(eligible=True)

    assert result.eligible is True
    assert result.reasons == ()


def test_eligible_result_rejects_contradictory_reasons() -> None:
    with pytest.raises(
        ValueError,
        match="eligible evaluation cannot contain rejection reasons",
    ):
        EvaluationResult(
            eligible=True,
            reasons=("insufficient_evidence",),
        )
