from epics.epic028_durable_node_ledger.node_ledger import NodeLedger
from epics.epic032_catchup_orchestrator.catchup_orchestrator import (
    CatchupOrchestrator,
)


def test_catchup_replaces_local_ledger(tmp_path):
    ...
    # tu test actual que ya pasa


def test_catchup_repairs_conflicting_node(tmp_path):

    db_path = tmp_path / "node.db"

    ledger = NodeLedger(db_path)

    ledger.append(
        {"sequence": 1, "event": "BOOTSTRAP"}
    )

    ledger.append(
        {"sequence": 2, "event": "BAD_EVENT"}
    )

    orchestrator = CatchupOrchestrator(ledger)

    orchestrator.catchup([
        {"sequence": 1, "event": "BOOTSTRAP"},
        {"sequence": 2, "event": "RECOVERED"},
        {"sequence": 3, "event": "RECOVERED"},
    ])

    assert ledger.all() == [
        {"sequence": 1, "event": "BOOTSTRAP"},
        {"sequence": 2, "event": "RECOVERED"},
        {"sequence": 3, "event": "RECOVERED"},
    ]

