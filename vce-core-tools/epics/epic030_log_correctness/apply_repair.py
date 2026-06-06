class ApplyRepair:

    def execute(
        self,
        canonical_log,
        divergent_log,
        plan
    ):

        if not plan[
            "repair_required"
        ]:

            return divergent_log

        truncate_from = plan[
            "truncate_from"
        ]

        pull_from = plan[
            "pull_suffix_from"
        ]

        repaired = (
            divergent_log[
                :truncate_from
            ]
            +
            canonical_log[
                pull_from:
            ]
        )

        return repaired
