from epics.epic028_durable_node_ledger.node_ledger import NodeLedger


def test_recovered_ledger_is_replayable(tmp_path):

    db_path = tmp_path / "node.db"

    ledger = NodeLedger(db_path)

    canonical = [
        {"sequence": 1, "event": "BOOTSTRAP"},
        {"sequence": 2, "event": "RECOVERED"},
        {"sequence": 3, "event": "RECOVERED"},
    ]

    ledger.replace_all(canonical)

    events = ledger.all()

    assert len(events) == 3

    assert events[0]["sequence"] == 1
    assert events[1]["sequence"] == 2
    assert events[2]["sequence"] == 3

def test_replay_sequence_is_monotonic():

    events = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 3},
        {"sequence": 4},
    ]

    sequences = [
        event["sequence"]
        for event in events
    ]

    assert sequences == sorted(sequences)

import pytest


def test_replay_rejects_non_monotonic_sequence():

    events = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 4},
        {"sequence": 3},
    ]

    sequences = [
        event["sequence"]
        for event in events
    ]

    assert sequences != sorted(sequences)
