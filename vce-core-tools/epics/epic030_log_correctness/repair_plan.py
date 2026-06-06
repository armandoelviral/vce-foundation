class ConflictRepairPlan:

    def create(
        self,
        resolution
    ):

        if not resolution[
            "repair_required"
        ]:

            return {
                "repair_required": False,
                "action": "NOOP"
            }

        return {
            "repair_required": True,
            "truncate_from": resolution[
                "conflict_index"
            ],
            "pull_suffix_from": resolution[
                "catch_up_from"
            ],
            "apply_suffix": True
        }
