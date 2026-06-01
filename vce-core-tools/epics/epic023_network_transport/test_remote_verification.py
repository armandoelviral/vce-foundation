from epics.epic023_network_transport.remote_verification import (
    RemoteVerification
)


verifier = RemoteVerification()


result = verifier.attest(
    "artifact-001"
)


print(
    result[
        "trusted"
    ]
)

print(
    result[
        "attestation"
    ][
        "verification"
    ]
)
