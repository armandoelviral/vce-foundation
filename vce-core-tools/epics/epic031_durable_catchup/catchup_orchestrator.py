from epics.epic030_log_correctness.conflict_resolver import (
    ConflictResolver
)

from epics.epic030_log_correctness.repair_plan import (
    ConflictRepairPlan
)

from epics.epic030_log_correctness.apply_repair import (
    ApplyRepair
)


class CatchupOrchestrator:

    def execute(
        self,
        canonical_log,
        local_log
    ):

        resolver = ConflictResolver()
        planner = ConflictRepairPlan()
        applier = ApplyRepair()

        resolution = resolver.resolve(
            canonical_log,
            local_log
        )

        plan = planner.create(
            resolution
        )

        repaired_log = applier.execute(
            canonical_log,
            local_log,
            plan
        )

        return {
            "resolution": resolution,
            "plan": plan,
            "repaired_log": repaired_log
        }
