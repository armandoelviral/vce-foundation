from epics.epic018_distributed_verification.verifier_identity import (
    VerifierIdentity
)

from epics.epic018_distributed_verification.verification_vote import (
    VerificationVote
)


identity = VerifierIdentity()

node = identity.create(
    "public-key-node-001"
)


voter = VerificationVote()


vote = voter.create(
    node,
    "artifact-hash-001",
    "APPROVE"
)


print(
    voter.verify(
        vote
    )
)


vote[
    "payload"
][
    "decision"
] = "REJECT"


print(
    voter.verify(
        vote
    )
)
