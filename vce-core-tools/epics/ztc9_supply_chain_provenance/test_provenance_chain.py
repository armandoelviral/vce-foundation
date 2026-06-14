from epics.ztc9_supply_chain_provenance.source_provenance_record import (
    SourceProvenanceRecord,
)

from epics.ztc9_supply_chain_provenance.build_provenance_record import (
    BuildProvenanceRecord,
)

from epics.ztc9_supply_chain_provenance.artifact_provenance_record import (
    ArtifactProvenanceRecord,
)

from epics.ztc9_supply_chain_provenance.provenance_chain import (
    ProvenanceChain,
)


def test_chain_binds_source_build_artifact():

    source = SourceProvenanceRecord(
        repository_url="repo",
        commit_sha="abc123",
        branch="main",
    )

    build = BuildProvenanceRecord(
        build_id="build-001",
        builder="github-actions",
        workflow="release.yml",
        source_commit="abc123",
    )

    artifact = ArtifactProvenanceRecord(
        artifact_id="artifact-001",
        artifact_hash="sha256-001",
        build_id="build-001",
    )

    chain = ProvenanceChain(
        source=source,
        build=build,
        artifact=artifact,
    )

    assert chain.source.commit_sha == "abc123"
    assert chain.build.source_commit == "abc123"
    assert chain.artifact.build_id == "build-001"


def test_chain_serializes():

    source = SourceProvenanceRecord(
        repository_url="repo",
        commit_sha="abc123",
        branch="main",
    )

    build = BuildProvenanceRecord(
        build_id="build-001",
        builder="github-actions",
        workflow="release.yml",
        source_commit="abc123",
    )

    artifact = ArtifactProvenanceRecord(
        artifact_id="artifact-001",
        artifact_hash="sha256-001",
        build_id="build-001",
    )

    chain = ProvenanceChain(
        source=source,
        build=build,
        artifact=artifact,
    )

    serialized = chain.to_dict()

    assert "source" in serialized
    assert "build" in serialized
    assert "artifact" in serialized
