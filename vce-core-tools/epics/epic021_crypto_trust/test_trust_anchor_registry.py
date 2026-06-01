from epics.epic021_crypto_trust.trust_anchor_registry import (
    TrustAnchorRegistry
)


registry = TrustAnchorRegistry()


fingerprint = registry.register(
    "root-anchor",
    "public-key-001"
)


print(
    registry.verify_anchor(
        fingerprint
    )
)


registry.revoke(
    fingerprint
)


print(
    registry.verify_anchor(
        fingerprint
    )
)


print(
    registry.count()
)
