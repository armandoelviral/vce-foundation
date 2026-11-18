from dataclasses import replace
from datetime import datetime, timezone

import pytest

from sp001.contracts.product001_document_version_binding import (
    Product001DocumentVersionBinding,
)
from sp001.contracts.product001_documentary_inputs import (
    Product001DocumentaryInputs,
)
from sp001.contracts.product001_planogram_admission_request import (
    Product001PlanogramAdmissionRequest,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
)
from sp001.contracts.knowledge_source_supersession import (
    KnowledgeSourceSupersessionGraph,
)
from sp001.services.product001_planogram_admission_service import (
    Product001PlanogramAdmissionService,
)

from test_knowledge_source_retrieval import (
    CONTENT,
    create_status,
    create_context,
    create_binding,
)


def make_request():
    return Product001PlanogramAdmissionRequest(
        source_id="POG-2026-DENIM-012",
        source_version=1,
        point_of_sale_id="POS-045",
        campaign_id="CAMP-SPRING-2026",
    )


def make_documentary_inputs(
    *,
    content=CONTENT,
    with_authority=True,
):
    source = create_status()

    return Product001DocumentaryInputs(
        source_status=source,
        content=content,
        effective_period=KnowledgeSourceEffectivePeriod(
            source_status=source,
            effective_from=datetime(
                2026, 3, 1, tzinfo=timezone.utc
            ),
        ),
        retrieval_context=create_context(),
        authority_bindings=(
            (create_binding(source),)
            if with_authority
            else ()
        ),
        supersession_graph=KnowledgeSourceSupersessionGraph(
            supersessions=()
        ),
    )


class TestBindingProvider:
    __test__ = False

    def resolve_binding(self, request):
        return Product001DocumentVersionBinding(
            source_id="POG-2026-DENIM-012",
            commercial_version=1,
            document_version="current",
            point_of_sale_id="POS-045",
            campaign_id="CAMP-SPRING-2026",
        )


class TestDocumentProvider:
    __test__ = False

    def __init__(self, inputs):
        self.inputs = inputs

    def resolve(self, request):
        return self.inputs


def test_admissible_document_reaches_evaluation():
    provider = TestDocumentProvider(
        make_documentary_inputs()
    )

    service = Product001PlanogramAdmissionService(
        binding_provider=TestBindingProvider(),
        documentary_provider=provider,
    )

    result = service.admit(request=make_request())

    assert result is not None


def test_tampered_document_is_rejected():
    provider = TestDocumentProvider(
        make_documentary_inputs(
            content=b"tampered planogram"
        )
    )

    service = Product001PlanogramAdmissionService(
        binding_provider=TestBindingProvider(),
        documentary_provider=provider,
    )

    with pytest.raises(ValueError):
        service.admit(request=make_request())


def test_document_without_authority_is_rejected():
    provider = TestDocumentProvider(
        make_documentary_inputs(
            with_authority=False
        )
    )

    service = Product001PlanogramAdmissionService(
        binding_provider=TestBindingProvider(),
        documentary_provider=provider,
    )

    with pytest.raises(ValueError):
        service.admit(request=make_request())
