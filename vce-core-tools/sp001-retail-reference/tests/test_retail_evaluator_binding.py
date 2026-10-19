from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBinding, RetailEvaluatorBindingSnapshot,
)


def make_binding():
    actor = RetailProcessActor(
        "ACTOR", "CUSTOMER", ActorType.HUMAN, "ORG",
        RetailProcessRole("ROLE", "CUSTOMER", "VM reviewer"),
    )
    return RetailEvaluatorBinding(
        binding_id="BINDING", revision=1,
        principal=AuthenticatedPrincipal("ISSUER", "SUBJECT"),
        actor=actor, case_id="CASE", valid_from=100, expires_at=200,
    )


def test_preserves_complete_actor_and_principal_without_equating_ids():
    binding = make_binding()
    assert binding.principal.subject == "SUBJECT"
    assert binding.actor.actor_id == "ACTOR"
    assert binding.actor.customer_id == "CUSTOMER"
    assert binding.actor.organization_id == "ORG"
    assert binding.actor.role.role_id == "ROLE"
    snapshot = RetailEvaluatorBindingSnapshot(binding, False)
    assert snapshot.binding is binding


def test_distinct_revisions_preserve_original():
    original = make_binding()
    revised = replace(original, revision=2, expires_at=300)
    assert original.revision == 1
    assert original.expires_at == 200
    assert revised != original


@pytest.mark.parametrize("field", ["binding_id", "case_id"])
@pytest.mark.parametrize("value", ["", " ", None, 1])
def test_rejects_invalid_text(field, value):
    with pytest.raises((TypeError, ValueError)):
        replace(make_binding(), **{field: value})


@pytest.mark.parametrize("value", [True, 1.0, "1", None, 0, -1])
def test_rejects_invalid_revision(value):
    with pytest.raises((TypeError, ValueError)):
        replace(make_binding(), revision=value)


@pytest.mark.parametrize("field", ["principal", "actor"])
@pytest.mark.parametrize("value", [None, "opaque-id"])
def test_rejects_invalid_nominal_identity(field, value):
    with pytest.raises(TypeError):
        replace(make_binding(), **{field: value})


@pytest.mark.parametrize("field", ["valid_from", "expires_at"])
@pytest.mark.parametrize("value", [True, 1.0, "100", None, -1])
def test_rejects_invalid_time(field, value):
    with pytest.raises((TypeError, ValueError)):
        replace(make_binding(), **{field: value})


@pytest.mark.parametrize("expires_at", [99, 100])
def test_rejects_empty_or_reversed_interval(expires_at):
    with pytest.raises(ValueError):
        replace(make_binding(), expires_at=expires_at)


@pytest.mark.parametrize("value", [0, 1, None, "false"])
def test_snapshot_requires_exact_revocation_flag(value):
    with pytest.raises(TypeError):
        RetailEvaluatorBindingSnapshot(make_binding(), value)


def test_snapshot_rejects_invalid_binding():
    with pytest.raises(TypeError):
        RetailEvaluatorBindingSnapshot(None, False)


def test_binding_and_snapshot_are_frozen():
    binding = make_binding()
    snapshot = RetailEvaluatorBindingSnapshot(binding, False)
    with pytest.raises(FrozenInstanceError):
        binding.case_id = "OTHER"
    with pytest.raises(FrozenInstanceError):
        snapshot.revoked = True
