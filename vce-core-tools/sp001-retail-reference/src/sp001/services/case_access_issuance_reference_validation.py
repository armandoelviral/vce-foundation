from sp001.contracts.case_access_issuance_preparation import (
    CaseAccessIssuancePreparation,
)
from sp001.contracts.case_access_grant_snapshot import CaseAccessGrantSnapshot
from sp001.contracts.federated_principal_binding_snapshot import (
    FederatedPrincipalBindingSnapshot,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal


class IssuanceReferenceValidationError(ValueError):
    """Reference inconsistency; no persistence or signing has occurred."""


def validate_issuance_references(
    *,
    preparation: CaseAccessIssuancePreparation,
    binding_snapshot: FederatedPrincipalBindingSnapshot | None,
    grant_snapshots: tuple[CaseAccessGrantSnapshot, ...],
    at_time: int,
) -> None:
    """Validate supplied snapshots; establish no transaction or authentication."""
    if not isinstance(preparation, CaseAccessIssuancePreparation):
        raise TypeError("preparation must be a CaseAccessIssuancePreparation")
    if binding_snapshot is not None and not isinstance(
        binding_snapshot, FederatedPrincipalBindingSnapshot
    ):
        raise TypeError("binding_snapshot has invalid type")
    if not isinstance(grant_snapshots, tuple):
        raise TypeError("grant_snapshots must be a tuple")
    if any(not isinstance(value, CaseAccessGrantSnapshot) for value in grant_snapshots):
        raise TypeError("grant_snapshots must contain CaseAccessGrantSnapshot")
    if isinstance(at_time, bool) or not isinstance(at_time, int):
        raise TypeError("at_time must be integer Unix seconds")
    if at_time < 0:
        raise ValueError("at_time must not be negative")

    def reject(reason):
        raise IssuanceReferenceValidationError(reason)

    if binding_snapshot is None:
        reject("binding_missing")
    current_binding = binding_snapshot.binding
    expected_binding = preparation.binding
    if current_binding.binding_id != expected_binding.binding_id:
        reject("binding_identity_mismatch")
    if current_binding.revision != expected_binding.revision:
        reject("binding_revision_conflict")
    if current_binding != expected_binding:
        reject("binding_content_conflict")
    if not binding_snapshot.active:
        reject("binding_inactive")

    payload = preparation.payload
    if not payload.issued_at <= at_time < payload.expires_at:
        reject("preparation_outside_validity")
    if payload.not_before > at_time:
        reject("preparation_not_yet_effective")

    snapshots = {}
    for snapshot in grant_snapshots:
        identifier = snapshot.grant.grant_id
        if identifier in snapshots:
            reject("duplicate_grant_snapshot")
        snapshots[identifier] = snapshot
    references = {value.grant_id: value for value in preparation.grant_references}
    if set(snapshots) != set(references):
        reject("grant_snapshot_set_mismatch")

    # Current grants identify the subject in the access issuer's namespace.
    expected_principal = AuthenticatedPrincipal(payload.issuer, payload.subject)
    for identifier, reference in references.items():
        snapshot = snapshots[identifier]
        grant = snapshot.grant
        if snapshot.revision != reference.revision:
            reject("grant_revision_conflict")
        if snapshot.revoked:
            reject("grant_revoked")
        if grant.principal != expected_principal:
            reject("grant_principal_mismatch")
        if grant.permission != reference.permission:
            reject("grant_permission_mismatch")
        if grant.expires_at != reference.expires_at:
            reject("grant_expiration_conflict")
        if not grant.valid_from <= at_time < grant.expires_at:
            reject("grant_outside_validity")
        if payload.not_before < grant.valid_from:
            reject("token_precedes_grant")
        if payload.expires_at > grant.expires_at:
            reject("token_outlives_grant")
