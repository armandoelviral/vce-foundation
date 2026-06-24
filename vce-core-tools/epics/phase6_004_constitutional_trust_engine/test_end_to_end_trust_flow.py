from epics.phase6_004_constitutional_trust_engine.trust_record import (
    TrustRecord,
)
from epics.phase6_004_constitutional_trust_engine.trust_registry import (
    TrustRegistry,
)
from epics.phase6_004_constitutional_trust_engine.trust_state import (
    TrustState,
)
from epics.phase6_004_constitutional_trust_engine.trust_verifier import (
    verify_trust,
)


def test_end_to_end_trust_flow():
    registry = TrustRegistry()

    registry.add(
        TrustRecord(
            "trust.001",
            "identity.001",
            10,
        )
    )

    registry.add(
        TrustRecord(
            "trust.002",
            "identity.001",
            20,
        )
    )

    state = TrustState.from_records(
        registry.records()
    )

    verification = verify_trust(state)

    assert verification["verified"] is True
    assert verification["total_score"] == 30
