import pytest

from sp001.contracts.subscriber_session_policy import (
    SubscriberSessionState, SessionObservation as Observation,
    SessionAction as Action, SessionTermination as Termination,
    evaluate_subscriber_session,
)


def evaluate(state, observation, now, session_id="SESSION-1"):
    return evaluate_subscriber_session(
        state=state, observation=observation, session_id=session_id, now=now,
    )


def initial():
    return SubscriberSessionState("SESSION-1", 100)


@pytest.mark.parametrize("observation, termination", [
    (Observation.AUTHENTICATION_REJECTED, Termination.AUTHENTICATION_REJECTED),
    (Observation.PERMISSION_WITHDRAWN, Termination.PERMISSION_WITHDRAWN),
])
def test_first_access_rejection_terminates_immediately(observation, termination):
    decision = evaluate(initial(), observation, 101)
    assert decision.action is Action.HIDE_AND_BLOCK
    assert decision.state.termination is termination


def test_first_failure_warns_second_blocks_without_claiming_revocation():
    first = evaluate(initial(), Observation.UNAVAILABLE, 104)
    assert first.action is Action.WARN
    assert first.state.termination is None
    second = evaluate(first.state, Observation.UNAVAILABLE, 108)
    assert second.action is Action.HIDE_AND_BLOCK
    assert second.state.termination is Termination.VERIFICATION_UNAVAILABLE


def test_success_before_deadline_resets_failure_count_and_deadline():
    first = evaluate(initial(), Observation.UNAVAILABLE, 105)
    success = evaluate(first.state, Observation.VALIDATED, 109)
    assert success.state.consecutive_failures == 0
    assert success.state.last_validated_at == 109
    assert evaluate(success.state, Observation.TICK, 118).action is Action.KEEP
    assert evaluate(success.state, Observation.TICK, 119).action is Action.HIDE_AND_BLOCK


def test_timer_blocks_even_without_a_second_network_result():
    decision = evaluate(initial(), Observation.TICK, 110)
    assert decision.action is Action.HIDE_AND_BLOCK
    assert decision.reason == "validation_deadline_exceeded"


def test_success_arriving_at_deadline_does_not_extend_session():
    decision = evaluate(initial(), Observation.VALIDATED, 110)
    assert decision.action is Action.HIDE_AND_BLOCK
    assert decision.state.last_validated_at == 100


def test_late_response_never_reactivates_terminated_session():
    terminated = evaluate(initial(), Observation.PERMISSION_WITHDRAWN, 101)
    late = evaluate(terminated.state, Observation.VALIDATED, 102)
    assert late.action is Action.IGNORE
    assert late.state == terminated.state


def test_other_session_cannot_update_or_revoke_active_session():
    for observation in (
        Observation.VALIDATED, Observation.PERMISSION_WITHDRAWN,
        Observation.UNAVAILABLE,
    ):
        decision = evaluate(initial(), observation, 105, "OLD-SESSION")
        assert decision.action is Action.IGNORE
        assert decision.state == initial()


@pytest.mark.parametrize("now", [True, -1, float("inf"), float("nan"), 99])
def test_invalid_or_regressing_clock_is_rejected(now):
    with pytest.raises(ValueError):
        evaluate(initial(), Observation.TICK, now)
