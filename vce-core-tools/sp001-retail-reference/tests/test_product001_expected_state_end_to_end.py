import pytest

from sp001.contracts.retail_expected_state import (
    RetailExpectedState,
)
from sp001.services.product001_planogram_admission_service import (
    Product001PlanogramAdmissionService,
)

from product001_admission_fixtures import (
    make_valid_admission_case,
)
from test_product001_admission_adversarial import (
    BindingProvider,
    DocumentaryProvider,
    binding,
    request,
)
from test_product001_admission_integration import (
    make_documentary_inputs,
)


def test_commercial_service_generates_expected_state():
    case = make_valid_admission_case()

    service = Product001PlanogramAdmissionService(
        binding_provider=BindingProvider(binding()),
        documentary_provider=DocumentaryProvider(
            make_documentary_inputs()
        ),
    )

    result = service.generate_expected_state(
        request=request(),
        expected_state_id="PRODUCT-001-EXPECTED-001",
        expected_state_version=1,
        rule=case.rule,
        snapshot=case.snapshot,
        provenance_bindings=case.bindings,
        planogram_dimension_ids=case.planogram_dimension_ids,
    )

    assert isinstance(result, RetailExpectedState)


def test_consumer_cannot_supply_retrieval_decision():
    case = make_valid_admission_case()

    service = Product001PlanogramAdmissionService(
        binding_provider=BindingProvider(binding()),
        documentary_provider=DocumentaryProvider(
            make_documentary_inputs()
        ),
    )

    with pytest.raises(TypeError):
        service.generate_expected_state(
            request=request(),
            expected_state_id="PRODUCT-001-EXPECTED-002",
            expected_state_version=1,
            rule=case.rule,
            snapshot=case.snapshot,
            provenance_bindings=case.bindings,
            planogram_dimension_ids=case.planogram_dimension_ids,
            retrieval_decision=case.decision,
        )
