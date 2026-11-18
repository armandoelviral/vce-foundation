from dataclasses import replace
from unittest.mock import patch

import pytest

from sp001.services.product001_planogram_admission_service import (
    Product001PlanogramAdmissionService,
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


@pytest.mark.parametrize(
    "invalid_binding",
    (
        replace(binding(), document_version="OTHER-VERSION"),
        replace(binding(), source_id="OTHER-SOURCE"),
        replace(binding(), point_of_sale_id="OTHER-STORE"),
        replace(binding(), campaign_id="OTHER-CAMPAIGN"),
        replace(binding(), commercial_version=2),
    ),
)
def test_invalid_identity_never_reaches_evaluator(
    invalid_binding,
):
    documentary_provider = DocumentaryProvider(
        make_documentary_inputs()
    )

    service = Product001PlanogramAdmissionService(
        binding_provider=BindingProvider(invalid_binding),
        documentary_provider=documentary_provider,
    )

    with patch(
        "sp001.services.product001_planogram_admission_service."
        "evaluate_knowledge_source_retrieval"
    ) as evaluator:
        with pytest.raises(ValueError):
            service.admit(request=request())

        evaluator.assert_not_called()
