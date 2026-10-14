from dataclasses import replace

import pytest

from test_sqlite_case_access_issuance_preparations import setup
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_issuance_request import CaseAccessIssuanceRequest
from sp001.contracts.case_access_issuance_policy import CaseAccessIssuancePolicy
from sp001.contracts.federated_issuance_context import ValidatedFederatedIssuanceContext
from sp001.contracts.case_access_grant_administration import GrantAdministrationAction
from sp001.services.case_access_issuance_reference_validation import (
    IssuanceReferenceValidationError,
)


def inputs(tmp_path):
    path, store, binding, command, template = setup(tmp_path)
    request = CaseAccessIssuanceRequest(
        "LIMITED-REQUEST", "CASE-001", template.payload.permissions[0].operation,
    )
    context = ValidatedFederatedIssuanceContext(
        binding.binding.external_principal, "issuance-service", 100, 100, 180,
    )
    policy = CaseAccessIssuancePolicy(
        "issuance-service", "access", "coordinator", "KEY-1", 60,
    )
    return store, binding, command, request, context, policy


def test_server_builds_payload_and_exact_replay_preserves_it(tmp_path):
    store, binding, _, request, context, policy = inputs(tmp_path)
    prepared = store.prepare_request(
        request=request, context=context, policy=policy, clock=lambda: 150,
    )
    assert prepared.binding == binding.binding
    assert prepared.payload.subject == "internal"
    assert prepared.payload.issuer == "access"
    assert prepared.payload.audience == "coordinator"
    assert prepared.payload.issued_at == 150
    assert prepared.payload.expires_at == 180
    assert prepared.payload.permissions == (request.permission,)
    assert prepared.grant_references[0].grant_id == "GRANT-1"
    assert prepared.grant_references[0].revision == 1
    assert prepared.payload.token_id
    assert store.prepare_request(
        request=request, context=context, policy=policy, clock=lambda: 151,
    ) == prepared
    assert store.read_prepared(request_id=request.request_id) == prepared


@pytest.mark.parametrize("bound", ["policy", "primary", "grant"])
def test_expiry_uses_earliest_limit(tmp_path, bound):
    store, _, _, request, context, policy = inputs(tmp_path)
    context = replace(context, expires_at=300)
    policy = replace(policy, max_lifetime_seconds=200)
    expected = 250
    if bound == "policy":
        policy = replace(policy, max_lifetime_seconds=10)
        expected = 160
    elif bound == "primary":
        context = replace(context, expires_at=170)
        expected = 170
    prepared = store.prepare_request(
        request=request, context=context, policy=policy, clock=lambda: 150,
    )
    assert prepared.payload.expires_at == expected


@pytest.mark.parametrize("kind", ["unknown_identity", "inactive_binding", "missing_grant"])
def test_missing_authority_creates_no_preparation(tmp_path, kind):
    store, binding, _, request, context, policy = inputs(tmp_path)
    if kind == "unknown_identity":
        context = replace(
            context, principal=AuthenticatedPrincipal("external", "OTHER"),
        )
    elif kind == "inactive_binding":
        store.put_binding(
            snapshot=replace(binding, binding=replace(binding.binding, revision=2),
                             active=False),
            expected_revision=1,
        )
    else:
        request = replace(request, case_id="OTHER")
    with pytest.raises(PermissionError):
        store.prepare_request(
            request=request, context=context, policy=policy, clock=lambda: 150,
        )
    assert store.read_prepared(request_id=request.request_id) is None


def test_same_request_identifier_cannot_change_case(tmp_path):
    store, _, _, request, context, policy = inputs(tmp_path)
    store.prepare_request(
        request=request, context=context, policy=policy, clock=lambda: 150,
    )
    with pytest.raises(ValueError, match="request_id conflicts"):
        store.prepare_request(
            request=replace(request, case_id="OTHER"),
            context=context, policy=policy, clock=lambda: 150,
        )


def test_revocation_prevents_replay(tmp_path):
    store, _, command, request, context, policy = inputs(tmp_path)
    prepared = store.prepare_request(
        request=request, context=context, policy=policy, clock=lambda: 150,
    )
    store.apply(record=replace(
        command, event_id="REVOKE-LIMITED",
        action=GrantAdministrationAction.REVOKE,
    ))
    with pytest.raises(IssuanceReferenceValidationError):
        store.prepare_request(
            request=request, context=context, policy=policy, clock=lambda: 150,
        )
    assert store.read_prepared(request_id=request.request_id) == prepared


def test_primary_expiry_before_commit_rolls_back_preparation(tmp_path):
    store, _, _, request, context, policy = inputs(tmp_path)
    times = iter((150, 180))
    with pytest.raises(PermissionError):
        store.prepare_request(
            request=request, context=context, policy=policy,
            clock=lambda: next(times),
        )
    assert store.read_prepared(request_id=request.request_id) is None
