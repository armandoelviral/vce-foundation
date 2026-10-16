from sp001.contracts.case_lifecycle_completion import CaseLifecycleCompletion
from sp001.contracts.case_lifecycle_execution_store import CaseLifecycleExecutionStore
from sp001.contracts.case_lifecycle_request import (
    CaseOpeningRequest, CaseTransitionRequest,
)
from sp001.services.case_lifecycle_recovery import match_case_lifecycle_completion

from time import perf_counter_ns

from sp001.services.case_state_subscription import CaseStateSubscription
from sp001.services.local_case_state_reader import LocalCaseStateReader

from sp001.models.capability_candidate import CapabilityCandidate
from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_authoritative_state_store import CaseAuthoritativeStateStore
from sp001.services.case_authoritative_state_reading import (
    read_case_authoritative_state as read_case_state,
)
from sp001.services.case_lifecycle_application import open_case
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
from sp001.runtime.transitions.expert_decision_to_operational_evidence import (
    ExpertDecisionToOperationalEvidenceTransition,
)
from sp001.runtime.transitions.objective_to_case import (
    ObjectiveToCaseTransition,
)
from sp001.runtime.transitions.recommendation_to_expert_decision import (
    RecommendationToExpertDecisionTransition,
)


class ScientificProductRuntime:
    """Coordinates Scientific Product lifecycle transitions."""

    def __init__(
        self,
        *,
        case_authoritative_state_store: CaseAuthoritativeStateStore | None = None,
        case_write_budget_ns: int | None = None,
        case_lifecycle_execution_store: CaseLifecycleExecutionStore | None = None,
    ) -> None:
        if (
            case_lifecycle_execution_store is not None
            and not isinstance(
                case_lifecycle_execution_store, CaseLifecycleExecutionStore,
            )
        ):
            raise TypeError(
                "case_lifecycle_execution_store must implement "
                "CaseLifecycleExecutionStore"
            )
        self._case_lifecycle_execution_store = case_lifecycle_execution_store
        if case_write_budget_ns is not None:
            if type(case_write_budget_ns) is not int:
                raise TypeError("case_write_budget_ns must be an integer")
            if case_write_budget_ns <= 0:
                raise ValueError("case_write_budget_ns must be positive")
            if (
                case_authoritative_state_store is None
                and case_lifecycle_execution_store is None
            ):
                raise ValueError("case write budget requires a durable store")
        self._case_write_budget_ns = case_write_budget_ns
        self._case_authoritative_state_store = (
            case_authoritative_state_store
        )
        self._objective_to_case = ObjectiveToCaseTransition()
        self._case_to_recommendation = CaseToRecommendationTransition()
        self._recommendation_to_expert_decision = (
            RecommendationToExpertDecisionTransition()
        )
        self._expert_decision_to_operational_evidence = (
            ExpertDecisionToOperationalEvidenceTransition()
        )

    def create_case(
        self,
        objective: Objective,
        *,
        case_id: str = "",
        scope: str = "",
    ) -> RuntimeResult:
        deadline_ns = (
            None if self._case_write_budget_ns is None
            else perf_counter_ns() + self._case_write_budget_ns
        )
        result = self._objective_to_case.execute(
            objective,
            case_id=case_id,
            scope=scope,
        )
        store = self._case_authoritative_state_store
        if store is None:
            return result

        case = result.output
        if not result.success or not isinstance(case, Case):
            return RuntimeResult(
                output=None,
                transition=result.transition,
                success=False,
            )

        options = (
            {} if deadline_ns is None
            else {"write_deadline_ns": deadline_ns}
        )
        try:
            state = open_case(
                store=store,
                case_id=case.case_id,
                objective_id=case.objective_id,
                scope=case.scope,
                transition_id=(
                    f"{case.case_id}:revision:1:CASE_OPENED"
                ),
                **options,
            )
        except (TypeError, ValueError):
            return RuntimeResult(
                output=None,
                transition=result.transition,
                success=False,
            )

        if state is None:
            return RuntimeResult(
                output=None,
                transition=result.transition,
                success=False,
            )
        return result

    def execute_case_lifecycle(
        self,
        *,
        request: CaseOpeningRequest | CaseTransitionRequest,
    ) -> CaseLifecycleCompletion | None:
        """Trusted execution entry; does not authenticate or authorize."""
        deadline_ns = (
            None if self._case_write_budget_ns is None
            else perf_counter_ns() + self._case_write_budget_ns
        )
        if type(request) not in (CaseOpeningRequest, CaseTransitionRequest):
            raise TypeError("request must be an exact lifecycle request")
        store = self._case_lifecycle_execution_store
        if store is None:
            raise RuntimeError("case lifecycle execution store is not configured")
        result = store.execute(
            request=request, write_deadline_ns=deadline_ns,
        )
        return match_case_lifecycle_completion(
            request=request, completion=result,
        )

    def recover_case_lifecycle(
        self,
        *,
        request: CaseOpeningRequest | CaseTransitionRequest,
    ) -> CaseLifecycleCompletion | None:
        """Recover the original result; does not authorize its delivery."""
        if type(request) not in (CaseOpeningRequest, CaseTransitionRequest):
            raise TypeError("request must be an exact lifecycle request")
        store = self._case_lifecycle_execution_store
        if store is None:
            raise RuntimeError("case lifecycle execution store is not configured")
        result = store.recover(request=request)
        return match_case_lifecycle_completion(
            request=request, completion=result,
        )

    def read_case_authoritative_state(
        self,
        *,
        case_id: str,
    ) -> CaseAuthoritativeState | None:
        store = self._case_authoritative_state_store
        if store is None:
            raise RuntimeError(
                "case authoritative state store is not configured"
            )
        return read_case_state(store=store, case_id=case_id)

    def subscribe_case_state(
        self,
        *,
        case_id: str,
    ) -> CaseStateSubscription:
        """Create a persistent in-process read session for one case."""
        store = self._case_authoritative_state_store
        if store is None:
            raise RuntimeError(
                "case authoritative state store is not configured"
            )
        return CaseStateSubscription(
            reader=LocalCaseStateReader(store=store),
            case_id=case_id,
        )

    def create_recommendation(
        self,
        case: Case,
    ) -> RuntimeResult:
        return self._case_to_recommendation.execute(case)

    def create_expert_decision(
        self,
        recommendation: Recommendation,
    ) -> RuntimeResult:
        return self._recommendation_to_expert_decision.execute(
            recommendation
        )

    def record_operational_evidence(
        self,
        decision: ExpertDecision,
    ) -> RuntimeResult:
        return self._expert_decision_to_operational_evidence.execute(
            decision
        )

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
