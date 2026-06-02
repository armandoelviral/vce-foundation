from epics.epic026_recovery.recovery_handshake import (
    RecoveryHandshake
)

handshake = RecoveryHandshake()

states = handshake.request_cluster_state(
    [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8002"
    ]
)

for state in states:
    print(state)
