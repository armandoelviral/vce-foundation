import inspect

import pytest

from sp001.contracts.product001_planogram_admission_request import (
    Product001PlanogramAdmissionRequest,
)
from sp001.services.product001_planogram_admission_service import (
    Product001PlanogramAdmissionService,
)


def test_public_admission_signature_excludes_authority_inputs():
    signature = inspect.signature(
        Product001PlanogramAdmissionService.admit
    )

    parameters = signature.parameters

    assert "request" in parameters

    forbidden = {
        "retrieval_decision",
        "source_status",
        "content",
        "effective_period",
        "authority_bindings",
        "supersession_graph",
        "retrieval_context",
        "resolver",
        "provider",
    }

    assert not forbidden.intersection(parameters)

    assert not any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    )


def test_request_cannot_carry_forged_decision():
    with pytest.raises(TypeError):
        Product001PlanogramAdmissionRequest(
            source_id="PLANOGRAM-001",
            source_version=1,
            point_of_sale_id="STORE-001",
            campaign_id="CAMPAIGN-001",
            retrieval_decision=object(),
        )


def test_request_cannot_carry_authority_bindings():
    with pytest.raises(TypeError):
        Product001PlanogramAdmissionRequest(
            source_id="PLANOGRAM-001",
            source_version=1,
            point_of_sale_id="STORE-001",
            campaign_id="CAMPAIGN-001",
            authority_bindings=(),
        )
