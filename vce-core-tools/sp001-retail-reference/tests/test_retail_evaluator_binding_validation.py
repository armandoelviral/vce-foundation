from dataclasses import replace

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBinding, RetailEvaluatorBindingSnapshot,
)
from sp001.services.retail_evaluator_binding_validation import (
    RetailEvaluatorBindingRejected,
    validate_retail_evaluator_binding,
)


def arguments():
    actor = RetailProcessActor(
        "ACTOR", "CUSTOMER", ActorType.HUMAN, "ORG",
        RetailProcessRole("ROLE", "CUSTOMER", "VM reviewer"),
    )
    principal = AuthenticatedPrincipal("ISSUER", "SUBJECT")
    binding = RetailEvaluatorBinding(
        "BINDING", 2, principal, actor, "CASE", 100, 200,
    )
    return dict(
        snapshot=RetailEvaluatorBindingSnapshot(binding, False),
        principal=principal, actor=actor, case_id="CASE",
        expected_binding_id="BINDING", expected_revision=2, at_time=150,
    )


def test_accepts_exact_supplied_binding_without_mutating_it():
    args = arguments()
    snapshot = args["snapshot"]
    assert validate_retail_evaluator_binding(**args) is None
    assert args["snapshot"] is snapshot
    assert snapshot.revoked is False
    assert snapshot.binding.revision == 2


@pytest.mark.parametrize("instant,accepted", [
    (99, False), (100, True), (199, True), (200, False),
])
def test_validity_boundaries(instant, accepted):
    args = arguments()
    args["at_time"] = instant
    if accepted:
        assert validate_retail_evaluator_binding(**args) is None
    else:
        with pytest.raises(
            RetailEvaluatorBindingRejected, match="outside_validity"
        ):
            validate_retail_evaluator_binding(**args)


@pytest.mark.parametrize("field,value,reason", [
    ("snapshot", None, "binding_missing"),
    ("expected_binding_id", "OTHER", "identity_mismatch"),
    ("expected_revision", 1, "revision_conflict"),
    ("case_id", "OTHER", "case_mismatch"),
    (
        "principal", AuthenticatedPrincipal("OTHER-ISSUER", "SUBJECT"),
        "principal_mismatch",
    ),
    (
        "principal", AuthenticatedPrincipal("ISSUER", "OTHER-SUBJECT"),
        "principal_mismatch",
    ),
])
def test_rejects_reference_mismatch(field, value, reason):
    args = arguments()
    args[field] = value
    with pytest.raises(RetailEvaluatorBindingRejected, match=reason):
        validate_retail_evaluator_binding(**args)


def test_rejects_revoked_snapshot():
    args = arguments()
    args["snapshot"] = replace(args["snapshot"], revoked=True)
    with pytest.raises(RetailEvaluatorBindingRejected, match="revoked"):
        validate_retail_evaluator_binding(**args)


@pytest.mark.parametrize("change", [
    "actor_id", "customer", "organization", "actor_type", "role",
])
def test_compares_complete_actor_not_only_actor_id(change):
    args = arguments()
    actor = args["actor"]
    if change == "actor_id":
        actor = replace(actor, actor_id="OTHER")
    elif change == "customer":
        actor = replace(
            actor, customer_id="OTHER-CUSTOMER",
            role=replace(actor.role, customer_id="OTHER-CUSTOMER"),
        )
    elif change == "organization":
        actor = replace(actor, organization_id="OTHER-ORG")
    elif change == "actor_type":
        actor = replace(actor, actor_type=ActorType.SYSTEM)
    else:
        actor = replace(
            actor, role=replace(actor.role, role_id="OTHER-ROLE")
        )
    args["actor"] = actor
    with pytest.raises(RetailEvaluatorBindingRejected, match="actor_mismatch"):
        validate_retail_evaluator_binding(**args)


@pytest.mark.parametrize("field,value,error", [
    ("snapshot", object(), TypeError),
    ("principal", "SUBJECT", TypeError),
    ("actor", "ACTOR", TypeError),
    ("case_id", "", ValueError),
    ("case_id", None, TypeError),
    ("expected_binding_id", " ", ValueError),
    ("expected_revision", True, TypeError),
    ("expected_revision", 0, ValueError),
    ("at_time", True, TypeError),
    ("at_time", -1, ValueError),
])
def test_rejects_invalid_arguments(field, value, error):
    args = arguments()
    args[field] = value
    with pytest.raises(error):
        validate_retail_evaluator_binding(**args)
