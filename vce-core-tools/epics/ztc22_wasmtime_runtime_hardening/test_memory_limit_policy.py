from epics.ztc22_wasmtime_runtime_hardening.memory_limit_policy import (
    MemoryLimitPolicy,
)


def test_accepts_memory_within_limit():

    policy = MemoryLimitPolicy(
        max_memory_bytes=65536,
    )

    assert policy.allow(
        requested_memory_bytes=32768,
    )


def test_accepts_exact_memory_limit():

    policy = MemoryLimitPolicy(
        max_memory_bytes=65536,
    )

    assert policy.allow(
        requested_memory_bytes=65536,
    )


def test_rejects_memory_over_limit():

    policy = MemoryLimitPolicy(
        max_memory_bytes=65536,
    )

    assert not policy.allow(
        requested_memory_bytes=131072,
    )
