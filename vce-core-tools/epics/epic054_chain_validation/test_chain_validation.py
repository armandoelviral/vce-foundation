from epics.epic049_state_provenance.provenance import (
    ProvenanceRecord,
)
from epics.epic054_chain_validation.chain_validator import (
    ChainValidator,
)


def test_validates_valid_chain():

    records = [
        ProvenanceRecord(
            snapshot_hash="aaa",
            parent_hash=None,
        ),
        ProvenanceRecord(
            snapshot_hash="bbb",
            parent_hash="aaa",
        ),
        ProvenanceRecord(
            snapshot_hash="ccc",
            parent_hash="bbb",
        ),
    ]

    validator = ChainValidator()

    assert validator.validate(records) is True


def test_rejects_missing_parent():

    records = [
        ProvenanceRecord(
            snapshot_hash="aaa",
            parent_hash=None,
        ),
        ProvenanceRecord(
            snapshot_hash="bbb",
            parent_hash="missing",
        ),
    ]

    validator = ChainValidator()

    assert validator.validate(records) is False
