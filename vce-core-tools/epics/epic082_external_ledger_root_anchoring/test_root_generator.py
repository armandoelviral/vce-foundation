from epics.epic082_external_ledger_root_anchoring.root_generator import (
    generate_ledger_root,
)


def build_records():

    return [
        {
            "sequence": 1,
            "artifact_hash": "artifact-001",
        },
        {
            "sequence": 2,
            "artifact_hash": "artifact-002",
        },
    ]


def test_root_generator_creates_ledger_root():

    root = generate_ledger_root(
        evidence_records=build_records(),
        region="us-east-1",
        generated_at="2026-06-10T00:00:00Z",
    )

    assert root.evidence_count == 2
    assert root.sequence_start == 1
    assert root.sequence_end == 2


def test_root_generator_is_deterministic():

    root_a = generate_ledger_root(
        evidence_records=build_records(),
        region="us-east-1",
        generated_at="2026-06-10T00:00:00Z",
    )

    root_b = generate_ledger_root(
        evidence_records=build_records(),
        region="us-east-1",
        generated_at="2026-06-10T00:00:00Z",
    )

    assert root_a.root_hash == root_b.root_hash


def test_root_generator_changes_when_records_change():

    root_a = generate_ledger_root(
        evidence_records=build_records(),
        region="us-east-1",
        generated_at="2026-06-10T00:00:00Z",
    )

    changed_records = build_records()
    changed_records.append(
        {
            "sequence": 3,
            "artifact_hash": "artifact-003",
        }
    )

    root_b = generate_ledger_root(
        evidence_records=changed_records,
        region="us-east-1",
        generated_at="2026-06-10T00:00:00Z",
    )

    assert root_a.root_hash != root_b.root_hash
    assert root_b.evidence_count == 3
