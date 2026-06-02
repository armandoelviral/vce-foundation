from epics.epic024_real_network.peer_transport import (
    PeerTransport
)


transport = PeerTransport()


results = transport.attest_many(
    [
        "http://127.0.0.1:8000"
    ],
    "artifact-001"
)

print(results)

print(
    len(results)
)

print(
    results[0]["trusted"]
)

print(
    results[0]["attestation"]
)
