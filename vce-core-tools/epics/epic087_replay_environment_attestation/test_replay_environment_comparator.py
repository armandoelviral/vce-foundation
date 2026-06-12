from epics.epic087_replay_environment_attestation.environment_fingerprint import (
    EnvironmentFingerprint,
)
from epics.epic087_replay_environment_attestation.replay_environment_comparator import (
    ReplayEnvironmentComparator,
)


def build_fingerprint(
    container_digest="sha256:container123",
    runtime_version="runtime-2.0.0",
    dependency_manifest_hash="deps-abc123",
    model_fingerprint="model-xyz789",
    policy_version="2.0.0",
    execution_profile="production",
):

    return EnvironmentFingerprint(
        container_digest=container_digest,
        runtime_version=runtime_version,
        dependency_manifest_hash=dependency_manifest_hash,
        model_fingerprint=model_fingerprint,
        policy_version=policy_version,
        execution_profile=execution_profile,
    )


def test_comparator_accepts_equivalent_environments():

    comparator = ReplayEnvironmentComparator()

    result = comparator.compare(
        build_fingerprint(),
        build_fingerprint(),
    )

    assert result["result"] == "ENVIRONMENT_EQUIVALENT"
    assert result["mismatches"] == []


def test_comparator_detects_container_mismatch():

    comparator = ReplayEnvironmentComparator()

    result = comparator.compare(
        build_fingerprint(),
        build_fingerprint(
            container_digest="sha256:different"
        ),
    )

    assert result["result"] == "ENVIRONMENT_MISMATCH"
    assert "container_digest" in result["mismatches"]


def test_comparator_detects_dependency_manifest_mismatch():

    comparator = ReplayEnvironmentComparator()

    result = comparator.compare(
        build_fingerprint(),
        build_fingerprint(
            dependency_manifest_hash="deps-different"
        ),
    )

    assert result["result"] == "ENVIRONMENT_MISMATCH"
    assert "dependency_manifest_hash" in result["mismatches"]


def test_comparator_detects_multiple_mismatches():

    comparator = ReplayEnvironmentComparator()

    result = comparator.compare(
        build_fingerprint(),
        build_fingerprint(
            runtime_version="runtime-3.0.0",
            execution_profile="staging",
        ),
    )

    assert result["result"] == "ENVIRONMENT_MISMATCH"
    assert "runtime_version" in result["mismatches"]
    assert "execution_profile" in result["mismatches"]
