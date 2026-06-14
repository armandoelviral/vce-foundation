from epics.ztc24_production_deployment_framework.deployment_manifest import (
    DeploymentManifest,
)


def test_manifest_contains_release_id():

    manifest = DeploymentManifest(
        release_id="release-001",
        artifact_hash="hash-001",
    )

    assert manifest.release_id == "release-001"


def test_manifest_contains_artifact_hash():

    manifest = DeploymentManifest(
        release_id="release-001",
        artifact_hash="hash-001",
    )

    assert manifest.artifact_hash == "hash-001"


def test_manifest_serializes():

    manifest = DeploymentManifest(
        release_id="release-001",
        artifact_hash="hash-001",
    )

    assert manifest.to_dict() == {
        "release_id": "release-001",
        "artifact_hash": "hash-001",
    }
