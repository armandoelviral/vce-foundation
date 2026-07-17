from has.runtime.evaluation_profiles import (
    EVALUATION_PROFILES,
)

from has.runtime.knowledge_state import (
    KnowledgeState,
)


def test_every_promotable_state_has_profile():

    assert (
        KnowledgeState.HYPOTHESIS
        in EVALUATION_PROFILES
    )

    assert (
        KnowledgeState.CANDIDATE_PRINCIPLE
        in EVALUATION_PROFILES
    )

    assert (
        KnowledgeState.PRINCIPLE
        in EVALUATION_PROFILES
    )


def test_profile_thresholds_are_monotonic():

    hypothesis = EVALUATION_PROFILES[
        KnowledgeState.HYPOTHESIS
    ]

    candidate = EVALUATION_PROFILES[
        KnowledgeState.CANDIDATE_PRINCIPLE
    ]

    principle = EVALUATION_PROFILES[
        KnowledgeState.PRINCIPLE
    ]

    assert (
        hypothesis.minimum_evidence
        <
        candidate.minimum_evidence
        <
        principle.minimum_evidence
    )
