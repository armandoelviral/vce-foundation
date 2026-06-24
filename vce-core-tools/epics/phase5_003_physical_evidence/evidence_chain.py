from epics.phase5_003_physical_evidence.evidence_record import (
    EvidenceRecord,
)


def build_evidence_chain(
    records: list[EvidenceRecord],
):
    return {
        "evidence_count": len(records),
        "hashes": [
            record.artifact_hash
            for record in records
        ],
    }
