from epics.epic092_deterministic_execution_policy.host_import_policy import (
    HostImportPolicy,
)


def test_memory_is_allowed():

    assert HostImportPolicy.is_allowed(
        "memory"
    )


def test_arithmetic_is_allowed():

    assert HostImportPolicy.is_allowed(
        "arithmetic"
    )


def test_clock_is_denied():

    assert not HostImportPolicy.is_allowed(
        "clock"
    )


def test_network_is_denied():

    assert not HostImportPolicy.is_allowed(
        "network"
    )


def test_filesystem_is_denied():

    assert not HostImportPolicy.is_allowed(
        "filesystem"
    )
