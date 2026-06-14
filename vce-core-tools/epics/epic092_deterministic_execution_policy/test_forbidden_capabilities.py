from epics.epic092_deterministic_execution_policy.forbidden_capabilities import (
    ForbiddenCapabilities,
)


def test_policy_contains_clock():
    assert "clock" in ForbiddenCapabilities.ALL


def test_policy_contains_random():
    assert "random" in ForbiddenCapabilities.ALL


def test_policy_contains_network():
    assert "network" in ForbiddenCapabilities.ALL


def test_policy_contains_filesystem():
    assert "filesystem" in ForbiddenCapabilities.ALL
