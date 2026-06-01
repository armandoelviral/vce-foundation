from epics.epic015_secure_runtime.failure_isolation import (
    FailureIsolation
)


isolation = FailureIsolation()


safe = isolation.protect(
    lambda: "OK"
)


failure = isolation.protect(
    lambda: 1 / 0
)


print(
    safe["success"]
)


print(
    failure["success"]
)


print(
    failure["contained"]
)
