from epics.epic033_conflict_aware_catchup.repair_plan import build_repair_plan


def test_detects_conflict():
    local = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 99},
    ]

    canonical = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 3},
    ]

    plan = build_repair_plan(local, canonical)

    assert plan["repair_required"] is True
    assert plan["conflict_index"] == 2


def test_computes_catch_up_point():
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

    plan = build_repair_plan(local, canonical)

    assert plan["repair_required"] is True
    assert plan["conflict_index"] == 2
    assert plan["catch_up_from"] == 2
