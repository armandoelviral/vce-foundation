from epics.epic021_crypto_trust.cryptographic_audit_chain import (
    CryptographicAuditChain
)


audit = CryptographicAuditChain()


audit.append(
    {
        "action": "SIGN",
        "artifact": "artifact-001"
    }
)


audit.append(
    {
        "action": "VERIFY",
        "artifact": "artifact-001"
    }
)


print(
    audit.verify()
)


audit.chain[0][
    "entry"
][
    "event"
][
    "artifact"
] = "tampered"


print(
    audit.verify()
)
