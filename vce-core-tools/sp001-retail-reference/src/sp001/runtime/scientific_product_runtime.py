from sp001.models.capability_candidate import CapabilityCandidate
from sp001.models.case import Case
from sp001.models.expert_decision import ExpertDecision
from sp001.models.governance_decision import GovernanceDecision
from sp001.models.institutional_capability import InstitutionalCapability
from sp001.models.objective import Objective
from sp001.models.operational_evidence import OperationalEvidence
from sp001.models.recommendation import Recommendation
from sp001.runtime.runtime_result import RuntimeResult
from sp001.runtime.transitions.case_to_recommendation import (
    CaseToRecommendationTransition,
)
from sp001.runtime.transitions.objective_to_case import (
    ObjectiveToCaseTransition,
)


class ScientificProductRuntime:
    """Coordinates Scientific Product lifecycle transitions."""

    def __init__(self) -> None:
        self._objective_to_case = ObjectiveToCaseTransition()
        self._case_to_recommendation = CaseToRecommendationTransition()

    def create_case(
        self,
        objective: Objective,
        *,
        case_id: str = "",
        scope: str = "",
    ) -> RuntimeResult:
        return self._objective_to_case.execute(
            objective,
            case_id=case_id,
            scope=scope,
        )

    def create_recommendation(self, case: Case) -> RuntimeResult:
        return self._case_to_recommendation.execute(case)

    def create_expert_decision(
        self,
        recommendation: Recommendation,
    ) -> ExpertDecision:
        return ExpertDecision()

    def record_operational_evidence(
        self,
        decision: ExpertDecision,
    ) -> OperationalEvidence:
        return OperationalEvidence()

    def create_capability_candidate(
        self,
        evidence: OperationalEvidence,
    ) -> CapabilityCandidate:
        return CapabilityCandidate()

    def create_governance_decision(
        self,
        candidate: CapabilityCandidate,
    ) -> GovernanceDecision:
        return GovernanceDecision()

    def create_institutional_capability(
        self,
        decision: GovernanceDecision,
    ) -> InstitutionalCapability:
        return InstitutionalCapability()
