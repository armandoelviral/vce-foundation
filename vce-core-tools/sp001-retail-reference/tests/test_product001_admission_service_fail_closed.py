from unittest.mock import patch

import pytest

from sp001.contracts.product001_planogram_admission_request import (
    Product001PlanogramAdmissionRequest,
)
from sp001.services.product001_planogram_admission_service import (
    Product001AdmissionUnavailableError,
    Product001PlanogramAdmissionService,
)


def make_request():
    return Product001PlanogramAdmissionRequest(
        source_id="PLANOGRAM-001",
        source_version=1,
        point_of_sale_id="STORE-001",
        campaign_id="CAMPAIGN-001",
    )


def test_valid_request_fails_closed_without_provider():
    service = Product001PlanogramAdmissionService()

    with pytest.raises(
        Product001AdmissionUnavailableError,
        match="trusted documentary resolution",
    ):
        service.admit(request=make_request())


def test_invalid_request_type_is_rejected():
    service = Product001PlanogramAdmissionService()

    with pytest.raises(
        TypeError,
        match="request must be",
    ):
        service.admit(request=object())


def test_unconfigured_service_never_generates_expected_state():
    service = Product001PlanogramAdmissionService()

    with patch(
        "sp001.services.product001_planogram_admission."
        "generate_retail_expected_state",
        side_effect=AssertionError(
            "expected state generation must not execute"
        ),
    ) as generator:
        with pytest.raises(
            Product001AdmissionUnavailableError,
        ):
            service.admit(request=make_request())

        generator.assert_not_called()
