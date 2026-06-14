from epics.ztc23_security_validation_framework.consensus_fault_injection import (
    ConsensusFaultInjection,
)


def test_no_faults_returns_original_votes():

    injector = ConsensusFaultInjection()

    votes = [
        True,
        True,
        True,
    ]

    result = injector.inject(
        votes=votes,
        fault_type=None,
    )

    assert result == votes


def test_offline_fault_removes_vote():

    injector = ConsensusFaultInjection()

    votes = [
        True,
        True,
        True,
    ]

    result = injector.inject(
        votes=votes,
        fault_type="offline",
    )

    assert len(result) == 2


def test_invalid_vote_fault_inverts_vote():

    injector = ConsensusFaultInjection()

    votes = [
        True,
        True,
        True,
    ]

    result = injector.inject(
        votes=votes,
        fault_type="invalid_vote",
    )

    assert result[0] is False


def test_unknown_fault_type_is_ignored():

    injector = ConsensusFaultInjection()

    votes = [
        True,
        True,
        True,
    ]

    result = injector.inject(
        votes=votes,
        fault_type="unknown",
    )

    assert result == votes
