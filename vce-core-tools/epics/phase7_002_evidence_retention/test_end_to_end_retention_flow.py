from epics.phase7_002_evidence_retention.retention_record import (
    RetentionRecord,
)
from epics.phase7_002_evidence_retention.retention_registry import (
    RetentionRegistry,
)
from epics.phase7_002_evidence_retention.retention_state import (
    RetentionState,
)
from epics.phase7_002_evidence_retention.retention_verifier import (
    verify_retention,
)


def test_end_to_end_retention_flow():
    registry = RetentionRegistry()

    registry.add(
        RetentionRecord(
            "ret.001",
            "evidence.001",
            25,
        )
    )

    registry.add(
        RetentionRecord(
            "ret.002",
            "evidence.002",
            10,
        )
    )

    state = RetentionState.from_records(
        registry.records()
    )

    verification = verify_retention(state)

    assert verification["verified"] is True
    assert verification["total_years"] == 35
