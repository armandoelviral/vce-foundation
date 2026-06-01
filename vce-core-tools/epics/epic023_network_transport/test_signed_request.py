from epics.epic023_network_transport.signed_request import (
    SignedRequest
)


signer = SignedRequest()


payload = {
    "artifact": "abc123",
    "action": "REMOTE_VERIFY"
}


envelope = signer.sign(
    payload
)


print(
    signer.verify(
        envelope
    )
)


envelope[
    "payload"
][
    "artifact"
] = "tampered"


print(
    signer.verify(
        envelope
    )
)
