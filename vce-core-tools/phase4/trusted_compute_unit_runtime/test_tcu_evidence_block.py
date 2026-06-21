from phase4.trusted_compute_unit_runtime.tcu_evidence_block import (
    TcuEvidenceBlock,
)


def test_contains_artifact_hash():

    block = TcuEvidenceBlock(
        artifact_hash="artifact-001",
        facts_hash="facts-001",
        input_commitment="input-001",
        purified_time_utc="2026-06-21T06:30:00Z",
    )

    assert block.artifact_hash == "artifact-001"


def test_contains_facts_hash():

    block = TcuEvidenceBlock(
        artifact_hash="artifact-001",
        facts_hash="facts-001",
        input_commitment="input-001",
        purified_time_utc="2026-06-21T06:30:00Z",
    )

    assert block.facts_hash == "facts-001"


def test_contains_input_commitment():

    block = TcuEvidenceBlock(
        artifact_hash="artifact-001",
        facts_hash="facts-001",
        input_commitment="input-001",
        purified_time_utc="2026-06-21T06:30:00Z",
    )

    assert block.input_commitment == "input-001"


def test_contains_time():

    block = TcuEvidenceBlock(
        artifact_hash="artifact-001",
        facts_hash="facts-001",
        input_commitment="input-001",
        purified_time_utc="2026-06-21T06:30:00Z",
    )

    assert block.purified_time_utc == "2026-06-21T06:30:00Z"


def test_serializes():

    block = TcuEvidenceBlock(
        artifact_hash="artifact-001",
        facts_hash="facts-001",
        input_commitment="input-001",
        purified_time_utc="2026-06-21T06:30:00Z",
    )

    assert block.to_dict() == {
        "artifact_hash": "artifact-001",
        "facts_hash": "facts-001",
        "input_commitment": "input-001",
        "purified_time_utc": "2026-06-21T06:30:00Z",
    }
