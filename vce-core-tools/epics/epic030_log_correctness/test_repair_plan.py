from epics.epic030_log_correctness.repair_plan import (
    ConflictRepairPlan
)


planner = ConflictRepairPlan()


plan = planner.create(
    {
        "repair_required": True,
        "conflict_index": 2,
        "catch_up_from": 2
    }
)


print(plan)


noop = planner.create(
    {
        "repair_required": False,
        "conflict_index": None,
        "catch_up_from": 5
    }
)


print(noop)
