from epics.epic087_replay_environment_attestation.runtime_configuration_snapshot import (
    RuntimeConfigurationSnapshot,
)


def build_snapshot():

    return RuntimeConfigurationSnapshot(
        runtime_version="runtime-2.0.0",
        policy_version="2.0.0",
        execution_profile="production",
        configuration_hash="config-hash-001",
    )


def test_snapshot_creation():

    snapshot = build_snapshot()

    assert (
        snapshot.runtime_version
        == "runtime-2.0.0"
    )


def test_snapshot_contains_policy_version():

    snapshot = build_snapshot()

    assert (
        snapshot.policy_version
        == "2.0.0"
    )


def test_snapshot_contains_execution_profile():

    snapshot = build_snapshot()

    assert (
        snapshot.execution_profile
        == "production"
    )


def test_snapshot_contains_configuration_hash():

    snapshot = build_snapshot()

    assert (
        snapshot.configuration_hash
        == "config-hash-001"
    )


def test_snapshot_serializes():

    snapshot = build_snapshot()

    payload = snapshot.to_dict()

    assert (
        payload["runtime_version"]
        == "runtime-2.0.0"
    )

    assert (
        payload["policy_version"]
        == "2.0.0"
    )

    assert (
        payload["configuration_hash"]
        == "config-hash-001"
    )
