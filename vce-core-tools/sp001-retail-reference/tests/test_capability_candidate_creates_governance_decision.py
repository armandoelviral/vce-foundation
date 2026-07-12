from sp001.models.capability_candidate import CapabilityCandidate
from sp001.models.governance_decision import GovernanceDecision


def test_capability_candidate_creates_governance_decision() -> None:
    candidate = CapabilityCandidate()

    decision = candidate.create_governance_decision()

    assert isinstance(decision, GovernanceDecision)
