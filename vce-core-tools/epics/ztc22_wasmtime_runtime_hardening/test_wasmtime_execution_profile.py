from epics.ztc22_wasmtime_runtime_hardening.wasmtime_execution_profile import (
    WasmtimeExecutionProfile,
)


def test_profile_contains_limits():

    profile = WasmtimeExecutionProfile(
        max_fuel=1000,
        max_memory_bytes=65536,
        allowed_imports={"env.log"},
        deterministic_required=True,
    )

    assert profile.max_fuel == 1000
    assert profile.max_memory_bytes == 65536


def test_profile_contains_allowed_imports():

    profile = WasmtimeExecutionProfile(
        max_fuel=1000,
        max_memory_bytes=65536,
        allowed_imports={"env.log"},
        deterministic_required=True,
    )

    assert "env.log" in profile.allowed_imports


def test_profile_serializes():

    profile = WasmtimeExecutionProfile(
        max_fuel=1000,
        max_memory_bytes=65536,
        allowed_imports={"env.log"},
        deterministic_required=True,
    )

    assert profile.to_dict() == {
        "max_fuel": 1000,
        "max_memory_bytes": 65536,
        "allowed_imports": ["env.log"],
        "deterministic_required": True,
    }
