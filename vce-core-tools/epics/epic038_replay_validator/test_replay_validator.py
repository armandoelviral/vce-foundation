from epics.epic038_replay_validator.replay_validator import (
    ReplayValidator,
)


def test_accepts_monotonic_sequence():

    validator = ReplayValidator()

    events = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 3},
        {"sequence": 4},
    ]

    assert validator.validate(events) is True


def test_rejects_non_monotonic_sequence():

    validator = ReplayValidator()

    events = [
        {"sequence": 1},
        {"sequence": 3},
        {"sequence": 2},
        {"sequence": 4},
    ]

    assert validator.validate(events) is False

def test_rejects_duplicate_sequence():

    validator = ReplayValidator()

    events = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 2},
        {"sequence": 3},
    ]

    assert validator.validate(events) is False


def test_rejects_sequence_gap():

    validator = ReplayValidator()

    events = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 4},
        {"sequence": 5},
    ]

    assert validator.validate(events) is False
