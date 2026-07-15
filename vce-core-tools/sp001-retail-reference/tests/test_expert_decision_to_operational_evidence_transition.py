from sp001.models.expert_decision import ExpertDecision
from sp001.models.operational_evidence import OperationalEvidence
from sp001.runtime.runtime_result import RuntimeResult
from sp001.runtime.transitions.expert_decision_to_operational_evidence import (
    ExpertDecisionToOperationalEvidenceTransition,
)


def test_expert_decision_to_operational_evidence_transition() -> None:

    transition = ExpertDecisionToOperationalEvidenceTransition()

    decision = ExpertDecision()

    result = transition.execute(decision)

    assert isinstance(result, RuntimeResult)
    assert result.success
    assert result.transition == "ExpertDecision->OperationalEvidence"
    assert isinstance(result.output, OperationalEvidence)
