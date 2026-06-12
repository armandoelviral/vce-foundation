from epics.epic082_external_ledger_root_anchoring.ledger_root import (
    LedgerRoot,
)


def build_root():

    return LedgerRoot(
        root_hash="root-hash-001",
        sequence_start=1,
        sequence_end=42,
        evidence_count=42,
        region="us-east-1",
        generated_at="2026-06-10T00:00:00Z",
    )


def test_ledger_root_creation():

    root = build_root()

    assert root.root_hash == "root-hash-001"
    assert root.sequence_start == 1
    assert root.sequence_end == 42


def test_ledger_root_contains_evidence_count():

    root = build_root()

    assert root.evidence_count == 42


def test_ledger_root_contains_region():

    root = build_root()

    assert root.region == "us-east-1"


def test_ledger_root_serializes_to_dict():

    root = build_root()

    payload = root.to_dict()

    assert payload["root_hash"] == "root-hash-001"
    assert payload["sequence_start"] == 1
    assert payload["sequence_end"] == 42
    assert payload["evidence_count"] == 42
