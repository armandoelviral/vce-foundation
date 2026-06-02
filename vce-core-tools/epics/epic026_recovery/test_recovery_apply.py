from epics.epic026_recovery.state_pull import (
    StatePull
)

from epics.epic026_recovery.recovery_apply import (
    RecoveryApply
)

pull = StatePull()

apply = RecoveryApply()

print("BEFORE")
print(
    apply.current()
)

remote_state = pull.pull(
    "http://127.0.0.1:8000"
)

apply.apply(
    remote_state
)

print()

print("AFTER")
print(
    apply.current()
)
