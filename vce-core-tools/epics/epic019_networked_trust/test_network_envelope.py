from epics.epic019_networked_trust.network_envelope import (
    NetworkEnvelope
)


network = NetworkEnvelope()


message = {
    "type": "CONSENSUS",
    "payload": {
        "artifact": "abc123"
    }
}


envelope = network.seal(
    message,
    "node-A"
)


print(
    network.verify(
        envelope
    )
)


envelope[
    "payload"
][
    "message"
][
    "payload"
][
    "artifact"
] = "tampered"


print(
    network.verify(
        envelope
    )
)
