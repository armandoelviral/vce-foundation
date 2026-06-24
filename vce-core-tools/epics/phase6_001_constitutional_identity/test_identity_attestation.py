from epics.phase6_001_constitutional_identity.identity_attestation import (
    attest_identity,
)
from epics.phase6_001_constitutional_identity.identity_record import (
    IdentityRecord,
)


def test_attests_identity():
    identity = IdentityRecord(
        "identity.001",
        "subject.001",
        "human",
    )

    result = attest_identity(identity)

    assert result["attested"] is True
