from epics.epic092_deterministic_execution_policy.determinism_validator import (
    DeterminismValidator,
)


def test_accepts_empty_capabilities():

    assert DeterminismValidator.validate(
        set()
    )


def test_rejects_clock():

    assert not DeterminismValidator.validate(
        {
            "clock",
        }
    )


def test_rejects_random():

    assert not DeterminismValidator.validate(
        {
            "random",
        }
    )


def test_rejects_multiple_forbidden_capabilities():

    assert not DeterminismValidator.validate(
        {
            "clock",
            "network",
            "filesystem",
        }
    )


def test_accepts_pure_compute():

    assert DeterminismValidator.validate(
        {
            "memory",
            "arithmetic",
        }
    )
