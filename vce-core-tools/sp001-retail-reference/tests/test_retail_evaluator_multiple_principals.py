from dataclasses import replace

import test_retail_report_attribution_admission as setup

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_evaluator_binding_change import (
    RetailEvaluatorBindingChange,
)


def test_distinct_principals_can_be_bound_to_same_declared_actor(tmp_path):
    (
        _, _, first_principal, _, first_binding,
        bindings, _, _, _, _, _,
    ) = setup.environment(tmp_path)

    second_principal = AuthenticatedPrincipal(
        first_principal.issuer,
        "SECOND-SUBJECT",
    )

    second_binding = replace(
        first_binding,
        binding_id="SECOND-BINDING",
        principal=second_principal,
    )

    assert bindings.apply(change=RetailEvaluatorBindingChange(
        "SECOND-BINDING-EVENT",
        RetailEvaluatorBindingSnapshot(second_binding, False),
        first_principal,
        150,
    ))

    first = bindings.read_snapshot(binding_id=first_binding.binding_id)
    second = bindings.read_snapshot(binding_id=second_binding.binding_id)

    assert first is not None
    assert second is not None
    assert first.binding.principal != second.binding.principal
    assert first.binding.actor == second.binding.actor
    assert first.binding.case_id == second.binding.case_id
    assert first.revoked is False
    assert second.revoked is False
