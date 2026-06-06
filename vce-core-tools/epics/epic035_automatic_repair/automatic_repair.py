from epics.epic033_conflict_aware_catchup.repair_plan import (
    build_repair_plan,
)

from epics.epic034_repair_executor.repair_executor import (
    execute_repair,
)


def automatic_repair(
    local,
    canonical,
):
    plan = build_repair_plan(
        local,
        canonical,
    )

    return execute_repair(
        canonical,
        plan,
    )
