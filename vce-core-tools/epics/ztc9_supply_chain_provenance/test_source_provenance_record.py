from epics.ztc9_supply_chain_provenance.source_provenance_record import (
    SourceProvenanceRecord,
)


def test_source_record_contains_repository_identity():

    record = SourceProvenanceRecord(
        repository_url="https://github.com/example/policy",
        commit_sha="abc123",
        branch="main",
    )

    assert record.repository_url == "https://github.com/example/policy"
    assert record.commit_sha == "abc123"
    assert record.branch == "main"


def test_source_record_serializes():

    record = SourceProvenanceRecord(
        repository_url="https://github.com/example/policy",
        commit_sha="abc123",
        branch="main",
    )

    assert record.to_dict() == {
        "repository_url": "https://github.com/example/policy",
        "commit_sha": "abc123",
        "branch": "main",
    }
