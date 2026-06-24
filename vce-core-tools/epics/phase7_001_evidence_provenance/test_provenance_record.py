from epics.phase7_001_evidence_provenance.provenance_record import (
    ProvenanceRecord,
)


def test_provenance_record_creation():
    record = ProvenanceRecord(
        provenance_id="prov.001",
        evidence_id="evidence.001",
        parent_id="root",
    )

    assert record.provenance_id == "prov.001"


def test_requires_provenance_id():
    try:
        ProvenanceRecord(
            "",
            "evidence.001",
            "root",
        )
        assert False
    except ValueError as exc:
        assert "provenance_id" in str(exc)
