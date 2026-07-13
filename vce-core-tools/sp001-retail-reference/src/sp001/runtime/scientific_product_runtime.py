from sp001.models.case import Case
from sp001.models.expert_decision import ExpertDecision
from sp001.models.objective import Objective
from sp001.models.recommendation import Recommendation
from sp001.models.operational_evidence import OperationalEvidence
from sp001.models.capability_candidate import CapabilityCandidate
from sp001.models.governance_decision import GovernanceDecision
from sp001.models.institutional_capability import InstitutionalCapability

class ScientificProductRuntime:
    """Coordinates Scientific Product lifecycle transitions."""

    def create_case(
        self,
        objective: Objective,
        *,
        case_id: str = "",
        scope: str = "",
    ) -> Case:
        return Case(
            case_id=case_id,
            objective_id=objective.objective_id,
            objective_title=objective.title,
            scope=scope,
        )

    def create_recommendation(self, case: Case) -> Recommendation:
        return Recommendation()

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
