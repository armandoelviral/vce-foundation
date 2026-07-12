from sp001.models.expert_decision import ExpertDecision
from sp001.models.operational_evidence import OperationalEvidence


def test_expert_decision_creates_operational_evidence() -> None:
    decision = ExpertDecision()

    evidence = decision.create_operational_evidence()

    assert isinstance(evidence, OperationalEvidence)
