from has.runtime.knowledge_state import KnowledgeState
from has.runtime.knowledge_transition_policy import (
    KnowledgeTransitionPolicy,
)


def test_allows_observation_to_hypothesis() -> None:
    policy = KnowledgeTransitionPolicy()

    assert policy.is_allowed(
        KnowledgeState.OBSERVATION,
        KnowledgeState.HYPOTHESIS,
    ) is True


def test_allows_hypothesis_to_candidate_principle() -> None:
    policy = KnowledgeTransitionPolicy()

    assert policy.is_allowed(
        KnowledgeState.HYPOTHESIS,
        KnowledgeState.CANDIDATE_PRINCIPLE,
    ) is True


def test_allows_candidate_principle_to_principle() -> None:
    policy = KnowledgeTransitionPolicy()

    assert policy.is_allowed(
        KnowledgeState.CANDIDATE_PRINCIPLE,
        KnowledgeState.PRINCIPLE,
    ) is True


def test_rejects_skipped_transition() -> None:
    policy = KnowledgeTransitionPolicy()

    assert policy.is_allowed(
        KnowledgeState.OBSERVATION,
        KnowledgeState.PRINCIPLE,
    ) is False


def test_rejects_backward_transition() -> None:
    policy = KnowledgeTransitionPolicy()

    assert policy.is_allowed(
        KnowledgeState.PRINCIPLE,
        KnowledgeState.OBSERVATION,
    ) is False


def test_rejects_same_state_transition() -> None:
    policy = KnowledgeTransitionPolicy()

    assert policy.is_allowed(
        KnowledgeState.HYPOTHESIS,
        KnowledgeState.HYPOTHESIS,
    ) is False


def test_supports_custom_transition_policy() -> None:
    policy = KnowledgeTransitionPolicy(
        allowed_transitions=frozenset({
            (
                KnowledgeState.OBSERVATION,
                KnowledgeState.CANDIDATE_PRINCIPLE,
            ),
        }),
    )

    assert policy.is_allowed(
        KnowledgeState.OBSERVATION,
        KnowledgeState.CANDIDATE_PRINCIPLE,
    ) is True

    assert policy.is_allowed(
        KnowledgeState.OBSERVATION,
        KnowledgeState.HYPOTHESIS,
    ) is False
