from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
    KnowledgeSourceRetrievalDecision,
)
from sp001.contracts.product001_documentary_inputs import (
    Product001DocumentaryInputs,
)
from sp001.contracts.product001_document_version_binding import (
    Product001DocumentVersionBinding,
)
from sp001.contracts.product001_planogram_admission_request import (
    Product001PlanogramAdmissionRequest,
)
from sp001.services.knowledge_source_retrieval import (
    evaluate_knowledge_source_retrieval,
)


class Product001AdmissionUnavailableError(RuntimeError):
    """Admission cannot proceed without trusted dependencies."""


class Product001PlanogramAdmissionService:
    """Evaluate documentary inputs after commercial identity validation.

    Provider trust remains a responsibility of host composition.
    """

    __slots__ = ("_binding_provider", "_documentary_provider")

    def __init__(
        self,
        *,
        binding_provider=None,
        documentary_provider=None,
    ):
        self._binding_provider = binding_provider
        self._documentary_provider = documentary_provider

    def admit(
        self,
        *,
        request: Product001PlanogramAdmissionRequest,
    ) -> KnowledgeSourceRetrievalDecision:
        if not isinstance(request, Product001PlanogramAdmissionRequest):
            raise TypeError(
                "request must be a Product001PlanogramAdmissionRequest"
            )

        if self._binding_provider is None:
            raise Product001AdmissionUnavailableError(
                "trusted documentary resolution is not configured"
            )

        binding = self._binding_provider.resolve_binding(request)

        if not isinstance(binding, Product001DocumentVersionBinding):
            raise ValueError(
                "document version binding is missing or invalid"
            )

        if (
            binding.source_id != request.source_id
            or binding.commercial_version != request.source_version
            or binding.point_of_sale_id != request.point_of_sale_id
            or binding.campaign_id != request.campaign_id
        ):
            raise ValueError(
                "commercial request does not match document binding"
            )

        if self._documentary_provider is None:
            raise Product001AdmissionUnavailableError(
                "trusted documentary resolution is not configured"
            )

        inputs = self._documentary_provider.resolve(request)

        if not isinstance(inputs, Product001DocumentaryInputs):
            raise ValueError("documentary inputs missing or invalid")

        source = inputs.source_status
        context = inputs.retrieval_context

        if (
            source.identity.source_id != binding.source_id
            or source.identity.source_version != binding.document_version
        ):
            raise ValueError("documentary identity mismatch")

        if source.scope.campaign_id != request.campaign_id:
            raise ValueError("documentary campaign mismatch")

        if context.point_of_sale_id != request.point_of_sale_id:
            raise ValueError("documentary store mismatch")

        if context.campaign_id != request.campaign_id:
            raise ValueError("retrieval campaign mismatch")

        decision = evaluate_knowledge_source_retrieval(
            source_status=inputs.source_status,
            content=inputs.content,
            effective_period=inputs.effective_period,
            retrieval_context=inputs.retrieval_context,
            authority_bindings=inputs.authority_bindings,
            supersession_graph=inputs.supersession_graph,
        )

        if decision.decision_status is not KnowledgeRetrievalDecisionStatus.INCLUDED:
            raise ValueError("documentary source excluded")

        return decision

    def generate_expected_state(
        self,
        *,
        request,
        expected_state_id,
        expected_state_version,
        rule,
        snapshot,
        provenance_bindings,
        planogram_dimension_ids,
    ):
        """Generate Retail state from a freshly evaluated document."""
        from sp001.services.product001_planogram_admission import (
            generate_admitted_planogram_expected_state,
        )

        decision = self.admit(request=request)

        return generate_admitted_planogram_expected_state(
            expected_state_id=expected_state_id,
            expected_state_version=expected_state_version,
            rule=rule,
            snapshot=snapshot,
            retrieval_decision=decision,
            provenance_bindings=provenance_bindings,
            planogram_dimension_ids=planogram_dimension_ids,
        )
