from epics.phase5_003_physical_evidence.evidence_chain import (
    build_evidence_chain,
)
from epics.phase5_003_physical_evidence.evidence_record import (
    EvidenceRecord,
)
from epics.phase5_003_physical_evidence.evidence_registry import (
    EvidenceRegistry,
)


def test_end_to_end_evidence_flow():
    registry = EvidenceRegistry()

    registry.add(
        EvidenceRecord(
            evidence_id="evidence.001",
            observation_id="obs.001",
            evidence_type="photo",
            artifact_hash="hash123",
        )
    )

    chain = build_evidence_chain(
        registry.records()
    )

    assert chain["evidence_count"] == 1
    assert chain["hashes"] == ["hash123"]
