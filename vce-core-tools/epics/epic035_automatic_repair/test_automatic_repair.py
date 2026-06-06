from epics.epic033_conflict_aware_catchup.repair_plan import (
    build_repair_plan,
)

from epics.epic034_repair_executor.repair_executor import (
    execute_repair,
)


def test_automatic_repair_workflow():

    local = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 99},
    ]

    canonical = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 3},
        {"sequence": 4},
    ]

    plan = build_repair_plan(
        local,
        canonical,
    )

    replacement = execute_repair(
        canonical,
        plan,
    )

    assert replacement == [
        {"sequence": 3},
        {"sequence": 4},
    ]
