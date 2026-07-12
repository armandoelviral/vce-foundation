from sp001.models.governance_decision import GovernanceDecision
from sp001.models.institutional_capability import InstitutionalCapability


def test_governance_decision_creates_institutional_capability() -> None:
    decision = GovernanceDecision()

    capability = decision.create_institutional_capability()

    assert isinstance(capability, InstitutionalCapability)
