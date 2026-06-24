from epics.phase8_001_temporal_validity.validity_record import (
    ValidityRecord,
)
from epics.phase8_001_temporal_validity.validity_registry import (
    ValidityRegistry,
)
from epics.phase8_001_temporal_validity.validity_state import (
    ValidityState,
)
from epics.phase8_001_temporal_validity.validity_verifier import (
    verify_validity,
)


def test_end_to_end_validity_flow():
    registry = ValidityRegistry()

    registry.add(
        ValidityRecord(
            "validity.001",
            "evidence.001",
            365,
        )
    )

    registry.add(
        ValidityRecord(
            "validity.002",
            "evidence.002",
            730,
        )
    )

    state = ValidityState.from_records(
        registry.records()
    )

    verification = verify_validity(state)

    assert verification["verified"] is True
    assert verification["total_days"] == 1095
