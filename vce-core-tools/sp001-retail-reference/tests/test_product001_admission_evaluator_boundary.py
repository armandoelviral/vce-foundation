from unittest.mock import patch

import pytest

from sp001.contracts.product001_planogram_admission_request import (
    Product001PlanogramAdmissionRequest,
)
from sp001.services.product001_planogram_admission_service import (
    Product001PlanogramAdmissionService,
)


def make_request():
    return Product001PlanogramAdmissionRequest(
        source_id="PLANOGRAM-001",
        source_version=1,
        point_of_sale_id="STORE-001",
        campaign_id="CAMPAIGN-001",
    )


def test_unconfigured_service_does_not_invoke_evaluator():
    service = Product001PlanogramAdmissionService()

    with patch(
        "sp001.services.knowledge_source_retrieval."
        "evaluate_knowledge_source_retrieval",
        side_effect=AssertionError(
            "unconfigured service invoked evaluator"
        ),
    ) as evaluator:
        with pytest.raises(RuntimeError):
            service.admit(request=make_request())

        evaluator.assert_not_called()


def test_unconfigured_service_does_not_invoke_adapter():
    service = Product001PlanogramAdmissionService()

    with patch(
        "sp001.services.product001_planogram_admission."
        "generate_admitted_planogram_expected_state",
        side_effect=AssertionError(
            "unconfigured service invoked adapter"
        ),
    ) as adapter:
        with pytest.raises(RuntimeError):
            service.admit(request=make_request())

        adapter.assert_not_called()
