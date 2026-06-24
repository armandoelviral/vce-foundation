from epics.phase6_001_constitutional_identity.identity_record import (
    IdentityRecord,
)


def attest_identity(identity: IdentityRecord):
    return {
        "attested": True,
        "identity_id": identity.identity_id,
        "subject_id": identity.subject_id,
    }
