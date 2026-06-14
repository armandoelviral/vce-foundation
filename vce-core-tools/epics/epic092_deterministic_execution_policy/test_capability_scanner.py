from epics.epic092_deterministic_execution_policy.capability_scanner import (
    CapabilityScanner,
)


def test_scanner_returns_empty_capabilities():

    capabilities = CapabilityScanner.scan(
        []
    )

    assert capabilities == set()


def test_scanner_detects_clock():

    capabilities = CapabilityScanner.scan(
        [
            "clock",
        ]
    )

    assert "clock" in capabilities


def test_scanner_detects_multiple_capabilities():

    capabilities = CapabilityScanner.scan(
        [
            "clock",
            "network",
            "filesystem",
        ]
    )

    assert capabilities == {
        "clock",
        "network",
        "filesystem",
    }
