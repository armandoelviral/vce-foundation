from sp001.models.expert_decision import ExpertDecision
from sp001.models.operational_evidence import OperationalEvidence
from sp001.runtime.runtime_result import RuntimeResult


class ExpertDecisionToOperationalEvidenceTransition:
    """Executes the transition from ExpertDecision to OperationalEvidence."""

    transition_name = "ExpertDecision->OperationalEvidence"

    def execute(
        self,
        decision: ExpertDecision,
    ) -> RuntimeResult:

        evidence = OperationalEvidence()

        return RuntimeResult(
            output=evidence,
            transition=self.transition_name,
            success=True,
        )
