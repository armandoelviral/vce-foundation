from epics.epic034_repair_executor.repair_executor import (
    execute_repair,
)


def test_builds_replacement_events():

    canonical = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 3},
        {"sequence": 4},
    ]

    plan = {
        "repair_required": True,
        "catch_up_from": 2,
    }

    replacement = execute_repair(
        canonical,
        plan,
    )

    assert replacement == [
        {"sequence": 3},
        {"sequence": 4},
    ]

