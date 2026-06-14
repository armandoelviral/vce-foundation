from epics.ztc22_wasmtime_runtime_hardening.import_restriction_policy import (
    ImportRestrictionPolicy,
)


def test_accepts_allowed_import():

    policy = ImportRestrictionPolicy(
        allowed_imports={
            "env.log",
            "env.clock",
        }
    )

    assert policy.allow(
        "env.log"
    )


def test_rejects_unknown_import():

    policy = ImportRestrictionPolicy(
        allowed_imports={
            "env.log",
            "env.clock",
        }
    )

    assert not policy.allow(
        "env.network"
    )


def test_accepts_multiple_allowed_imports():

    policy = ImportRestrictionPolicy(
        allowed_imports={
            "env.log",
            "env.clock",
        }
    )

    assert policy.allow(
        "env.clock"
    )
