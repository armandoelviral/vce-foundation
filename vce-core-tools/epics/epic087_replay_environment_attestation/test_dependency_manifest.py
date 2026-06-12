from epics.epic087_replay_environment_attestation.dependency_manifest import (
    DependencyManifest,
)


def build_manifest():

    return DependencyManifest(
        manifest_id="deps-001",
        dependencies={
            "python": "3.14.5",
            "pytest": "9.0.3",
            "cryptography": "42.0.0",
        },
    )


def test_dependency_manifest_creation():

    manifest = build_manifest()

    assert manifest.manifest_id == "deps-001"


def test_dependency_manifest_counts_dependencies():

    manifest = build_manifest()

    assert manifest.dependency_count() == 3


def test_dependency_manifest_returns_dependency_version():

    manifest = build_manifest()

    assert manifest.get_version(
        "cryptography"
    ) == "42.0.0"


def test_dependency_manifest_returns_none_for_unknown_dependency():

    manifest = build_manifest()

    assert manifest.get_version(
        "unknown"
    ) is None


def test_dependency_manifest_serializes():

    manifest = build_manifest()

    payload = manifest.to_dict()

    assert payload["manifest_id"] == "deps-001"
    assert payload["dependencies"]["python"] == "3.14.5"
