from epics.epic038_replay_validator.replay_validator import (
    ReplayValidator,
)
from epics.epic039_safe_repair.safe_repair_executor import (
    SafeRepairExecutor,
)


def test_rejects_illegal_repair_plan():
    validator = ReplayValidator()

    events = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 2},
    ]

    assert validator.validate(events) is False


def test_accepts_valid_repair():
    executor = SafeRepairExecutor()

    events = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 3},
    ]

    assert executor.execute(events) is True


def test_rejects_invalid_repair():
    executor = SafeRepairExecutor()

    events = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 2},
    ]

    assert executor.execute(events) is False
