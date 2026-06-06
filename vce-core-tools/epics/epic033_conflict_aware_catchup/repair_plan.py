def build_repair_plan(local, canonical):
    for index, (local_event, canonical_event) in enumerate(
        zip(local, canonical)
    ):
        if local_event != canonical_event:
            return {
                "repair_required": True,
                "conflict_index": index,
                "catch_up_from": index,
            }

    if len(local) != len(canonical):
        return {
            "repair_required": True,
            "conflict_index": min(
                 len(local), 
                 len(canonical)),
        }

        return {
            "repair_required": True,
            "conflict_index": conflict_index,
            "catch_up_from": conflict_index,
        } 

        return {
            "repair_required": False,
            "conflict_index": None,
            "catch_up_from": None,
        }
