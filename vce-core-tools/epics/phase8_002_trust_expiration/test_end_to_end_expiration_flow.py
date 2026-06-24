from epics.phase8_002_trust_expiration.expiration_record import (
    ExpirationRecord,
)
from epics.phase8_002_trust_expiration.expiration_registry import (
    ExpirationRegistry,
)
from epics.phase8_002_trust_expiration.expiration_state import (
    ExpirationState,
)
from epics.phase8_002_trust_expiration.expiration_verifier import (
    verify_expiration,
)


def test_end_to_end_expiration_flow():
    registry = ExpirationRegistry()

    registry.add(
        ExpirationRecord(
            "exp.001",
            "trust.001",
            365,
        )
    )

    registry.add(
        ExpirationRecord(
            "exp.002",
            "trust.002",
            30,
        )
    )

    state = ExpirationState.from_records(
        registry.records()
    )

    verification = verify_expiration(state)

    assert verification["verified"] is True
    assert verification["total_remaining_days"] == 395
