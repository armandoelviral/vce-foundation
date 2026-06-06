from epics.epic031_durable_catchup.catchup_orchestrator import (
    CatchupOrchestrator
)


orchestrator = CatchupOrchestrator()


canonical_log = [
    {"sequence": 1},
    {"sequence": 2},
    {"sequence": 3},
    {"sequence": 4},
    {"sequence": 5}
]


local_log = [
    {"sequence": 1},
    {"sequence": 2},
    {"sequence": 99}
]


result = orchestrator.execute(
    canonical_log,
    local_log
)


print(
    result["resolution"]
)

print(
    result["plan"]
)

print(
    result["repaired_log"]
)

