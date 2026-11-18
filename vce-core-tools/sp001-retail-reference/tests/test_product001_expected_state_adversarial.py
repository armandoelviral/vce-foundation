from dataclasses import replace
from unittest.mock import patch

import pytest

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


ADAPTER = (
    "sp001.services.product001_planogram_admission."
    "generate_admitted_planogram_expected_state"
)


def generate(service):
    case = make_valid_admission_case()

    return service.generate_expected_state(
        request=request(),
        expected_state_id="PRODUCT-001-EXPECTED-ADVERSARIAL",
        expected_state_version=1,
        rule=case.rule,
        snapshot=case.snapshot,
        provenance_bindings=case.bindings,
        planogram_dimension_ids=case.planogram_dimension_ids,
    )


@pytest.mark.parametrize(
    "document",
    (
        make_documentary_inputs(
            content=b"tampered planogram"
        ),
        make_documentary_inputs(
            with_authority=False
        ),
    ),
    ids=("tampered-content", "missing-authority"),
)
def test_invalid_document_never_generates_retail_state(
    document,
):
    provider = DocumentaryProvider(document)

    service = Product001PlanogramAdmissionService(
        binding_provider=BindingProvider(binding()),
        documentary_provider=provider,
    )

    with patch(ADAPTER) as adapter:
        with pytest.raises(ValueError):
            generate(service)

        adapter.assert_not_called()

    assert provider.calls == 1


@pytest.mark.parametrize(
    "invalid_binding",
    (
        replace(binding(), source_id="OTHER-SOURCE"),
        replace(binding(), document_version="OTHER-VERSION"),
        replace(binding(), point_of_sale_id="OTHER-STORE"),
        replace(binding(), campaign_id="OTHER-CAMPAIGN"),
    ),
    ids=(
        "wrong-source",
        "wrong-version",
        "wrong-store",
        "wrong-campaign",
    ),
)
def test_invalid_binding_never_generates_retail_state(
    invalid_binding,
):
    provider = DocumentaryProvider(
        make_documentary_inputs()
    )

    service = Product001PlanogramAdmissionService(
        binding_provider=BindingProvider(invalid_binding),
        documentary_provider=provider,
    )

    with patch(ADAPTER) as adapter:
        with pytest.raises(ValueError):
            generate(service)

        adapter.assert_not_called()

    expected_calls = (
        1 if invalid_binding.document_version != "current"
        else 0
    )

    assert provider.calls == expected_calls


def test_missing_documentary_provider_fails_closed():
    service = Product001PlanogramAdmissionService(
        binding_provider=BindingProvider(binding()),
    )

    with patch(ADAPTER) as adapter:
        with pytest.raises(RuntimeError):
            generate(service)

        adapter.assert_not_called()
