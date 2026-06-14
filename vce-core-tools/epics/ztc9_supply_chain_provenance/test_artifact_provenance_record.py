from epics.ztc9_supply_chain_provenance.artifact_provenance_record import (
    ArtifactProvenanceRecord,
)


def test_artifact_record_contains_identity():

    record = ArtifactProvenanceRecord(
        artifact_id="artifact-001",
        artifact_hash="sha256-001",
        build_id="build-001",
    )

    assert record.artifact_id == "artifact-001"
    assert record.artifact_hash == "sha256-001"
    assert record.build_id == "build-001"


def test_artifact_record_serializes():

    record = ArtifactProvenanceRecord(
        artifact_id="artifact-001",
        artifact_hash="sha256-001",
        build_id="build-001",
    )

    assert record.to_dict() == {
        "artifact_id": "artifact-001",
        "artifact_hash": "sha256-001",
        "build_id": "build-001",
    }
