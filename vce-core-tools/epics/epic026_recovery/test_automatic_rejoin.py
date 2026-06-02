from epics.epic026_recovery.automatic_rejoin import (
    AutomaticRejoin
)

rejoin = AutomaticRejoin()

result = rejoin.execute(
    [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8002"
    ]
)

print(result)
