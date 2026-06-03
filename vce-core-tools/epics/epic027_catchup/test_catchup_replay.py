from epics.epic027_catchup.catchup_replay import (
    CatchupReplay
)

catchup = CatchupReplay()

result = catchup.execute(
    [
        {
            "sequence": 1,
            "event": "BOOTSTRAP"
        },
        {
            "sequence": 2,
            "event": "ATTESTATION"
        },
        {
            "sequence": 3,
            "event": "ATTESTATION"
        },
        {
            "sequence": 4,
            "event": "ATTESTATION"
        }
    ]
)

print(result)
