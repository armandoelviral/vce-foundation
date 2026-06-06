from epics.epic030_log_correctness.log_matcher import (
    LogMatcher
)


class ConflictResolver:

    def resolve(
        self,
        canonical_log,
        divergent_log
    ):

        matcher = LogMatcher()

        result = matcher.compare(
            canonical_log,
            divergent_log
        )

        if result["match"]:

            return {
                "repair_required": False,
                "conflict_index": None,
                "canonical_prefix": canonical_log,
                "catch_up_from": len(canonical_log)
            }

        conflict_index = result["conflict_index"]

        return {
            "repair_required": True,
            "conflict_index": conflict_index,
            "canonical_prefix": canonical_log[
                :conflict_index
            ],
            "catch_up_from": conflict_index
        }
