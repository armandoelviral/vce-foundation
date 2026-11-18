from dataclasses import replace

import pytest

from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
)
from sp001.contracts.product001_document_version_binding import (
    Product001DocumentVersionBinding,
)
from sp001.contracts.product001_planogram_admission_request import (
    Product001PlanogramAdmissionRequest,
)
from sp001.services.product001_planogram_admission_service import (
    Product001PlanogramAdmissionService,
)

from test_product001_admission_integration import (
    make_documentary_inputs,
)


def request():
    return Product001PlanogramAdmissionRequest(
        source_id="POG-2026-DENIM-012",
        source_version=1,
        point_of_sale_id="POS-045",
        campaign_id="CAMP-SPRING-2026",
    )


def binding():
    return Product001DocumentVersionBinding(
        source_id="POG-2026-DENIM-012",
        commercial_version=1,
        document_version="current",
        point_of_sale_id="POS-045",
        campaign_id="CAMP-SPRING-2026",
    )


class BindingProvider:
    def __init__(self, value):
        self.value = value

    def resolve_binding(self, request):
        return self.value


class DocumentaryProvider:
    def __init__(self, value):
        self.value = value
        self.calls = 0

    def resolve(self, request):
        self.calls += 1
        return self.value


def service(document, selected_binding=None):
    provider = DocumentaryProvider(document)

    admission = Product001PlanogramAdmissionService(
        binding_provider=BindingProvider(
            binding() if selected_binding is None else selected_binding
        ),
        documentary_provider=provider,
    )

    return admission, provider


def test_valid_document_is_explicitly_included():
    admission, provider = service(make_documentary_inputs())

    result = admission.admit(request=request())

    assert result.decision_status is KnowledgeRetrievalDecisionStatus.INCLUDED
    assert provider.calls == 1


@pytest.mark.parametrize(
    "field,value",
    (
        ("source_id", "OTHER-SOURCE"),
        ("document_version", "OTHER-VERSION"),
        ("point_of_sale_id", "OTHER-STORE"),
        ("campaign_id", "OTHER-CAMPAIGN"),
    ),
)
def test_incorrect_binding_rejected_before_document_resolution(
    field,
    value,
):
    altered = replace(binding(), **{field: value})

    admission, provider = service(
        make_documentary_inputs(),
        selected_binding=altered,
    )

    with pytest.raises(ValueError):
        admission.admit(request=request())

    if field == "document_version":
        # Document identity is checked after resolution.
        assert provider.calls == 1
    else:
        # Commercial identity is checked before resolution.
        assert provider.calls == 0


def test_tampered_content_rejected():
    admission, provider = service(
        make_documentary_inputs(
            content=b"tampered planogram"
        )
    )

    with pytest.raises(ValueError):
        admission.admit(request=request())

    assert provider.calls == 1


def test_missing_documentary_authority_rejected():
    admission, provider = service(
        make_documentary_inputs(
            with_authority=False
        )
    )

    with pytest.raises(ValueError):
        admission.admit(request=request())

    assert provider.calls == 1
