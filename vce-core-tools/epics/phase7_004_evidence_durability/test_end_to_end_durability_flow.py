from epics.phase7_004_evidence_durability.durability_record import (
    DurabilityRecord,
)
from epics.phase7_004_evidence_durability.durability_registry import (
    DurabilityRegistry,
)
from epics.phase7_004_evidence_durability.durability_state import (
    DurabilityState,
)
from epics.phase7_004_evidence_durability.durability_verifier import (
    verify_durability,
)


def test_end_to_end_durability_flow():
    registry = DurabilityRegistry()

    registry.add(
        DurabilityRecord(
            "dur.001",
            "evidence.001",
            50,
        )
    )

    registry.add(
        DurabilityRecord(
            "dur.002",
            "evidence.002",
            25,
        )
    )

    state = DurabilityState.from_records(
        registry.records()
    )

    verification = verify_durability(state)

    assert verification["verified"] is True
    assert verification["total_years"] == 75
