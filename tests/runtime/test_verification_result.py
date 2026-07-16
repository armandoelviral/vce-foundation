import pytest

from has.runtime.verification_result import VerificationResult


def test_valid_result_has_no_reasons() -> None:
    result = VerificationResult(
        valid=True,
    )

    assert result.valid is True
    assert result.reasons == ()


def test_invalid_result_accepts_reasons() -> None:
    result = VerificationResult(
        valid=False,
        reasons=("transition_not_allowed",),
    )

    assert result.valid is False
    assert result.reasons == (
        "transition_not_allowed",
    )


def test_valid_result_rejects_contradictory_reasons() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "valid verification cannot contain "
            "rejection reasons"
        ),
    ):
        VerificationResult(
            valid=True,
            reasons=("transition_not_allowed",),
        )
