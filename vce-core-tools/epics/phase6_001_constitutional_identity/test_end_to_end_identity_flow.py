from epics.phase6_001_constitutional_identity.identity_attestation import (
    attest_identity,
)
from epics.phase6_001_constitutional_identity.identity_record import (
    IdentityRecord,
)
from epics.phase6_001_constitutional_identity.identity_registry import (
    IdentityRegistry,
)
from epics.phase6_001_constitutional_identity.identity_state import (
    IdentityState,
)
from epics.phase6_001_constitutional_identity.identity_verifier import (
    verify_identity_state,
)


def test_end_to_end_identity_flow():
    registry = IdentityRegistry()

    registry.add(
        IdentityRecord(
            "identity.001",
            "subject.001",
            "human",
        )
    )

    attestation = attest_identity(
        registry.records()[0]
    )

    state = IdentityState.from_records(
        registry.records()
    )

    verification = verify_identity_state(state)

    assert attestation["attested"] is True
    assert verification["verified"] is True
    assert verification["total_identities"] == 1
