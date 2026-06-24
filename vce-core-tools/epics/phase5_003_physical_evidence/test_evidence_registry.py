from epics.phase5_003_physical_evidence.evidence_record import EvidenceRecord
from epics.phase5_003_physical_evidence.evidence_registry import EvidenceRegistry


def test_registry_stores_evidence():
    registry = EvidenceRegistry()

    registry.add(
        EvidenceRecord(
            "evidence.001",
            "obs.001",
            "photo",
            "abc123",
        )
    )

    assert len(registry.records()) == 1


def test_rejects_duplicate():
    registry = EvidenceRegistry()

    record = EvidenceRecord(
        "evidence.001",
        "obs.001",
        "photo",
        "abc123",
    )

    registry.add(record)

    try:
        registry.add(record)
        assert False
    except ValueError:
        assert True


def test_returns_copy():
    registry = EvidenceRegistry()

    registry.add(
        EvidenceRecord(
            "evidence.001",
            "obs.001",
            "photo",
            "abc123",
        )
    )

    items = registry.records()
    items.clear()

    assert len(registry.records()) == 1
