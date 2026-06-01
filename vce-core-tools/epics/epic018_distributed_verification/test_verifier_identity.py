from epics.epic018_distributed_verification.verifier_identity import (
    VerifierIdentity
)


factory = VerifierIdentity()


node = factory.create(
    "public-key-node-001"
)


print(
    factory.verify(
        node
    )
)


node[
    "public_key"
] = "tampered"


print(
    factory.verify(
        node
    )
)
