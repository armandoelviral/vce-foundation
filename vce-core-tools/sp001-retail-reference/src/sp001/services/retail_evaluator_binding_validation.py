from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_process_actor import RetailProcessActor
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBindingSnapshot,
)


class RetailEvaluatorBindingRejected(ValueError):
    """Supplied binding does not satisfy attribution requirements."""


def validate_retail_evaluator_binding(
    *,
    snapshot: RetailEvaluatorBindingSnapshot | None,
    principal: AuthenticatedPrincipal,
    actor: RetailProcessActor,
    case_id: str,
    expected_binding_id: str,
    expected_revision: int,
    at_time: int,
) -> None:
    """Validate supplied state only; no authentication, storage or permission grant."""
    if snapshot is not None and not isinstance(
        snapshot, RetailEvaluatorBindingSnapshot
    ):
        raise TypeError("snapshot must be a RetailEvaluatorBindingSnapshot")
    if not isinstance(principal, AuthenticatedPrincipal):
        raise TypeError("principal must be an AuthenticatedPrincipal")
    if not isinstance(actor, RetailProcessActor):
        raise TypeError("actor must be a RetailProcessActor")

    for name, value in (
        ("case_id", case_id),
        ("expected_binding_id", expected_binding_id),
    ):
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        if not value.strip():
            raise ValueError(f"{name} must not be empty")
    if type(expected_revision) is not int:
        raise TypeError("expected_revision must be an integer")
    if expected_revision < 1:
        raise ValueError("expected_revision must be positive")
    if type(at_time) is not int:
        raise TypeError("at_time must be integer Unix seconds")
    if at_time < 0:
        raise ValueError("at_time must be nonnegative")

    if snapshot is None:
        raise RetailEvaluatorBindingRejected("binding_missing")

    binding = snapshot.binding
    checks = (
        (binding.binding_id == expected_binding_id, "binding_identity_mismatch"),
        (binding.revision == expected_revision, "binding_revision_conflict"),
        (binding.principal == principal, "binding_principal_mismatch"),
        (binding.actor == actor, "binding_actor_mismatch"),
        (binding.case_id == case_id, "binding_case_mismatch"),
        (not snapshot.revoked, "binding_revoked"),
        (
            binding.valid_from <= at_time < binding.expires_at,
            "binding_outside_validity",
        ),
    )
    for satisfied, reason in checks:
        if not satisfied:
            raise RetailEvaluatorBindingRejected(reason)
