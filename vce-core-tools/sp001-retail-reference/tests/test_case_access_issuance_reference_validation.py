from dataclasses import replace

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import CaseAccessPermission, CaseAccessOperation
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_snapshot import CaseAccessGrantSnapshot
from sp001.contracts.case_access_issuance_preparation import (
    FederatedPrincipalBinding, IssuanceGrantReference,
    CaseAccessTokenPayload, CaseAccessIssuancePreparation,
)
from sp001.contracts.federated_principal_binding_snapshot import (
    FederatedPrincipalBindingSnapshot,
)
from sp001.services.case_access_issuance_reference_validation import (
    validate_issuance_references, IssuanceReferenceValidationError,
)


def values():
    permission = CaseAccessPermission("CASE-001", CaseAccessOperation.READ_STATE)
    binding = FederatedPrincipalBinding(
        "BINDING-1", 3,
        AuthenticatedPrincipal("external-issuer", "external-subject"),
        "internal-subject",
    )
    payload = CaseAccessTokenPayload(
        "access-issuer", "internal-subject", "coordinator",
        100, 100, 200, "TOKEN-1", (permission,),
    )
    preparation = CaseAccessIssuancePreparation(
        "REQUEST-1", binding, payload, "KEY-1",
        (IssuanceGrantReference("GRANT-1", 2, permission, 250),),
    )
    grant = CaseAccessGrant(
        "GRANT-1", AuthenticatedPrincipal("access-issuer", "internal-subject"),
        permission, 90, 250,
    )
    return preparation, FederatedPrincipalBindingSnapshot(binding, True), (
        CaseAccessGrantSnapshot(grant, 2, False),
    )


def validate(preparation, binding, grants, at_time=150):
    return validate_issuance_references(
        preparation=preparation, binding_snapshot=binding,
        grant_snapshots=grants, at_time=at_time,
    )


def test_matching_references_validate_without_mutation():
    preparation, binding, grants = values()
    before = (preparation, binding, grants)
    assert validate(preparation, binding, grants) is None
    assert (preparation, binding, grants) == before


@pytest.mark.parametrize("kind,reason", [
    ("missing", "binding_missing"),
    ("identity", "binding_identity_mismatch"),
    ("revision", "binding_revision_conflict"),
    ("external_subject", "binding_content_conflict"),
    ("internal_subject", "binding_content_conflict"),
    ("inactive", "binding_inactive"),
])
def test_binding_inconsistencies_are_rejected(kind, reason):
    preparation, binding, grants = values()
    if kind == "missing":
        binding = None
    elif kind == "identity":
        binding = replace(binding, binding=replace(binding.binding, binding_id="OTHER"))
    elif kind == "revision":
        binding = replace(binding, binding=replace(binding.binding, revision=4))
    elif kind == "external_subject":
        binding = replace(binding, binding=replace(
            binding.binding,
            external_principal=AuthenticatedPrincipal("external-issuer", "OTHER"),
        ))
    elif kind == "internal_subject":
        binding = replace(binding, binding=replace(binding.binding, internal_subject="OTHER"))
    else:
        binding = replace(binding, active=False)
    with pytest.raises(IssuanceReferenceValidationError, match=reason):
        validate(preparation, binding, grants)


@pytest.mark.parametrize("kind,reason", [
    ("revision", "grant_revision_conflict"),
    ("revoked", "grant_revoked"),
    ("principal", "grant_principal_mismatch"),
    ("permission", "grant_permission_mismatch"),
    ("expiration", "grant_expiration_conflict"),
    ("future", "grant_outside_validity"),
    ("token_start", "token_precedes_grant"),
])
def test_grant_inconsistencies_are_rejected(kind, reason):
    preparation, binding, grants = values()
    snapshot = grants[0]
    if kind == "revision":
        snapshot = replace(snapshot, revision=3)
    elif kind == "revoked":
        snapshot = replace(snapshot, revoked=True)
    elif kind == "principal":
        snapshot = replace(snapshot, grant=replace(
            snapshot.grant, principal=AuthenticatedPrincipal("access-issuer", "OTHER"),
        ))
    elif kind == "permission":
        snapshot = replace(snapshot, grant=replace(
            snapshot.grant,
            permission=CaseAccessPermission("OTHER", CaseAccessOperation.READ_STATE),
        ))
    elif kind == "expiration":
        snapshot = replace(snapshot, grant=replace(snapshot.grant, expires_at=240))
    elif kind == "future":
        snapshot = replace(snapshot, grant=replace(snapshot.grant, valid_from=160))
    else:
        snapshot = replace(snapshot, grant=replace(snapshot.grant, valid_from=110))
    with pytest.raises(IssuanceReferenceValidationError, match=reason):
        validate(preparation, binding, (snapshot,))


@pytest.mark.parametrize("kind", ["missing", "extra", "duplicate"])
def test_snapshot_set_must_match_exactly(kind):
    preparation, binding, grants = values()
    if kind == "missing":
        grants = ()
    elif kind == "extra":
        grants += (replace(grants[0], grant=replace(grants[0].grant, grant_id="OTHER")),)
    else:
        grants *= 2
    with pytest.raises(IssuanceReferenceValidationError):
        validate(preparation, binding, grants)


@pytest.mark.parametrize("at_time", [99, 200])
def test_preparation_validity_boundaries_are_rejected(at_time):
    preparation, binding, grants = values()
    with pytest.raises(IssuanceReferenceValidationError, match="outside_validity"):
        validate(preparation, binding, grants, at_time)


def test_validity_at_start_is_accepted():
    preparation, binding, grants = values()
    assert validate(preparation, binding, grants, 100) is None


def test_same_revision_does_not_allow_changed_binding_content():
    preparation, binding, grants = values()
    changed = replace(binding.binding, external_principal=AuthenticatedPrincipal(
        "other-issuer", binding.binding.external_principal.subject,
    ))
    with pytest.raises(IssuanceReferenceValidationError, match="content_conflict"):
        validate(preparation, replace(binding, binding=changed), grants)
