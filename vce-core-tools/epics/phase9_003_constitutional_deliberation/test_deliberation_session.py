from epics.phase9_003_constitutional_deliberation.deliberation_session import (
    deliberation_ready,
)


def test_deliberation_ready():
    assert deliberation_ready(7) is True


def test_deliberation_not_ready():
    assert deliberation_ready(0) is False
