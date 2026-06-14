from epics.ztc22_wasmtime_runtime_hardening.deterministic_execution_policy import (
    DeterministicExecutionPolicy,
)


def test_accepts_execution_without_nondeterminism():

    policy = DeterministicExecutionPolicy()

    assert policy.allow(
        uses_system_time=False,
        uses_randomness=False,
    )


def test_rejects_system_time_dependency():

    policy = DeterministicExecutionPolicy()

    assert not policy.allow(
        uses_system_time=True,
        uses_randomness=False,
    )


def test_rejects_randomness_dependency():

    policy = DeterministicExecutionPolicy()

    assert not policy.allow(
        uses_system_time=False,
        uses_randomness=True,
    )


def test_rejects_multiple_nondeterministic_sources():

    policy = DeterministicExecutionPolicy()

    assert not policy.allow(
        uses_system_time=True,
        uses_randomness=True,
    )
