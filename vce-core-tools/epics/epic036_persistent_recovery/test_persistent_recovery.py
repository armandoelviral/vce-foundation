from epics.epic028_durable_node_ledger.node_ledger import NodeLedger
from epics.epic033_conflict_aware_catchup.repair_plan import (
    build_repair_plan,
)
from epics.epic034_repair_executor.repair_executor import (
    execute_repair,
)


def test_end_to_end_persistent_recovery(tmp_path):
    db_path = tmp_path / "node.db"

    ledger = NodeLedger(db_path)

    ledger.append({
        "sequence": 1,
        "event": "BOOTSTRAP",
    })

    ledger.append({
        "sequence": 2,
        "event": "BAD_EVENT",
    })

    canonical = [
        {"sequence": 1, "event": "BOOTSTRAP"},
        {"sequence": 2, "event": "RECOVERED"},
        {"sequence": 3, "event": "RECOVERED"},
    ]

    local = ledger.all()

    plan = build_repair_plan(local, canonical)

    replacement = execute_repair(canonical, plan)

    assert replacement == [
        {"sequence": 2, "event": "RECOVERED"},
        {"sequence": 3, "event": "RECOVERED"},
    ]

    ledger.replace_all(canonical)

    assert ledger.all() == canonical
