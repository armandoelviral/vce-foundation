from epics.ztc7_quantum_resilient_evidence.dual_verification_policy import (
    DualVerificationPolicy,
)


def test_strict_now_requires_both():

    assert DualVerificationPolicy.verify(
        classical_valid=True,
        pqc_valid=True,
        mode="strict_now",
    )

    assert not DualVerificationPolicy.verify(
        classical_valid=True,
        pqc_valid=False,
        mode="strict_now",
    )


def test_future_resilience_accepts_either():

    assert DualVerificationPolicy.verify(
        classical_valid=True,
        pqc_valid=False,
        mode="future_resilience",
    )

    assert DualVerificationPolicy.verify(
        classical_valid=False,
        pqc_valid=True,
        mode="future_resilience",
    )


def test_rejects_when_both_invalid():

    assert not DualVerificationPolicy.verify(
        classical_valid=False,
        pqc_valid=False,
        mode="future_resilience",
    )
