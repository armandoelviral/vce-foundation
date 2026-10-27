from dataclasses import replace

import test_retail_report_attribution_admission as setup

from sp001.contracts.retail_process_role import RetailProcessRole


def test_same_actor_id_with_different_role_is_not_equal_as_full_actor(tmp_path):
    _, _, _, report, _, _, _, _, _, _, _ = setup.environment(tmp_path)

    original = report.evaluations[0].evaluator

    other_role = RetailProcessRole(
        "ANOTHER-ROLE",
        original.customer_id,
        "Independent reviewer",
    )
    changed_role = replace(original, role=other_role)

    assert changed_role != original
    assert changed_role.actor_id == original.actor_id
    assert changed_role.customer_id == original.customer_id
    assert changed_role.organization_id == original.organization_id
    assert changed_role.role != original.role
