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

from epics.ztc9_supply_chain_provenance.provenance_verifier import (
    ProvenanceVerifier,
)


def test_end_to_end_supply_chain_provenance_flow():

    source = SourceProvenanceRecord(
        repository_url="https://github.com/example/policy",
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

    assert ProvenanceVerifier.verify(chain)
