from epics.ztc9_supply_chain_provenance.build_provenance_record import (
    BuildProvenanceRecord,
)


def test_build_record_contains_builder_identity():

    record = BuildProvenanceRecord(
        build_id="build-001",
        builder="github-actions",
        workflow="release.yml",
        source_commit="abc123",
    )

    assert record.build_id == "build-001"
    assert record.builder == "github-actions"
    assert record.workflow == "release.yml"
    assert record.source_commit == "abc123"


def test_build_record_serializes():

    record = BuildProvenanceRecord(
        build_id="build-001",
        builder="github-actions",
        workflow="release.yml",
        source_commit="abc123",
    )

    assert record.to_dict() == {
        "build_id": "build-001",
        "builder": "github-actions",
        "workflow": "release.yml",
        "source_commit": "abc123",
    }
