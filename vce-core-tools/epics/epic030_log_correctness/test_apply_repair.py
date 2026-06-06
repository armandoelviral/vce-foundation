from epics.epic030_log_correctness.apply_repair import (
    ApplyRepair
)


repair = ApplyRepair()


canonical_log = [
    {"sequence": 1},
    {"sequence": 2},
    {"sequence": 3},
    {"sequence": 4},
    {"sequence": 5}
]


divergent_log = [
    {"sequence": 1},
    {"sequence": 2},
    {"sequence": 99}
]


plan = {
    "repair_required": False,
    "truncate_from": 2,
    "pull_suffix_from": 2,
    "apply_suffix": True
}


result = repair.execute(
    canonical_log,
    divergent_log,
    plan
)


print(result)
