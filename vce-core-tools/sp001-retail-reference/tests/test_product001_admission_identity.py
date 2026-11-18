import pytest

from sp001.contracts.product001_document_version_binding import (
    Product001DocumentVersionBinding,
)
from sp001.contracts.product001_planogram_admission_request import (
    Product001PlanogramAdmissionRequest,
)
from sp001.services.product001_planogram_admission_service import (
    Product001PlanogramAdmissionService,
)


def make_request(**changes):
    values = {
        "source_id": "POG-2026-DENIM-012",
        "source_version": 1,
        "point_of_sale_id": "POS-045",
        "campaign_id": "CAMP-SPRING-2026",
    }
    values.update(changes)
    return Product001PlanogramAdmissionRequest(**values)


def make_binding(**changes):
    values = {
        "source_id": "POG-2026-DENIM-012",
        "commercial_version": 1,
        "document_version": "current",
        "point_of_sale_id": "POS-045",
        "campaign_id": "CAMP-SPRING-2026",
    }
    values.update(changes)
    return Product001DocumentVersionBinding(**values)


class BindingProvider:
    def __init__(self, binding):
        self.binding = binding

    def resolve_binding(self, request):
        return self.binding


@pytest.mark.parametrize(
    "request_change",
    (
        {"source_id": "OTHER-SOURCE"},
        {"source_version": 2},
        {"point_of_sale_id": "OTHER-STORE"},
        {"campaign_id": "OTHER-CAMPAIGN"},
    ),
)
def test_mismatched_commercial_identity_is_rejected(
    request_change,
):
    service = Product001PlanogramAdmissionService(
        binding_provider=BindingProvider(make_binding())
    )

    with pytest.raises(ValueError):
        service.admit(
            request=make_request(**request_change)
        )


def test_missing_binding_is_rejected():
    service = Product001PlanogramAdmissionService(
        binding_provider=BindingProvider(None)
    )

    with pytest.raises(ValueError):
        service.admit(request=make_request())
