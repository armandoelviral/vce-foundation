from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import CaseAccessPermission, CaseAccessOperation
from sp001.contracts.case_access_issuance_preparation import (
    FederatedPrincipalBinding, IssuanceGrantReference,
    CaseAccessTokenPayload, CaseAccessIssuancePreparation,
)


PERMISSION = CaseAccessPermission("CASE-001", CaseAccessOperation.READ_STATE)


def preparation():
    binding = FederatedPrincipalBinding(
        "BINDING-001", 1,
        AuthenticatedPrincipal("https://external.example", "external-subject"),
        "internal-001",
    )
    payload = CaseAccessTokenPayload(
        issuer="https://access.example", subject="internal-001",
        audience="sp001-coordinator",
        issued_at=100, not_before=100, expires_at=200,
        token_id="TOKEN-001", permissions=(PERMISSION,),
    )
    return CaseAccessIssuancePreparation(
        request_id="REQUEST-001", binding=binding, payload=payload,
        signing_key_id="KEY-001",
        grant_references=(IssuanceGrantReference(
            "GRANT-001", 1, PERMISSION, 200,
        ),),
    )


def test_external_and_access_issuer_are_explicitly_distinct():
    value = preparation()
    assert value.binding.external_principal.issuer == "https://external.example"
    assert value.payload.issuer == "https://access.example"
    assert value.payload.subject == value.binding.internal_subject


def test_claims_use_versioned_profile_and_exact_permissions():
    assert preparation().payload.to_claims() == {
        "iss": "https://access.example", "sub": "internal-001",
        "aud": "sp001-coordinator",
        "iat": 100, "nbf": 100, "exp": 200,
        "jti": "TOKEN-001", "sp001_profile": "case-access.v1",
        "case_permissions": [{"case_id": "CASE-001", "operation": "READ_STATE"}],
    }


def test_exported_claims_do_not_mutate_payload():
    value = preparation().payload
    claims = value.to_claims()
    claims["case_permissions"].clear()
    assert value.permissions == (PERMISSION,)


def test_subject_mismatch_is_rejected():
    value = preparation()
    with pytest.raises(ValueError):
        replace(value, payload=replace(value.payload, subject="other"))


def test_token_cannot_outlive_grant():
    value = preparation()
    with pytest.raises(ValueError):
        replace(value, payload=replace(value.payload, expires_at=201))


def test_missing_or_extra_permission_evidence_is_rejected():
    value = preparation()
    extra = CaseAccessPermission("OTHER", CaseAccessOperation.READ_STATE)
    with pytest.raises(ValueError):
        replace(value, grant_references=(replace(
            value.grant_references[0], permission=extra,
        ),))


def test_duplicate_grant_ids_are_rejected():
    value = preparation()
    with pytest.raises(ValueError):
        replace(value, grant_references=value.grant_references * 2)


@pytest.mark.parametrize("field,value", [
    ("issued_at", True), ("not_before", "100"),
    ("expires_at", -1), ("expires_at", 100),
    ("token_id", ""), ("permissions", ()),
    ("permissions", (PERMISSION, PERMISSION)),
])
def test_invalid_payload_is_rejected(field, value):
    with pytest.raises((TypeError, ValueError)):
        replace(preparation().payload, **{field: value})


def test_payload_permission_order_is_explicit():
    other = CaseAccessPermission("AAA", CaseAccessOperation.READ_STATE)
    with pytest.raises(ValueError, match="canonical"):
        replace(preparation().payload, permissions=(PERMISSION, other))


def test_contract_values_are_immutable():
    value = preparation()
    with pytest.raises(FrozenInstanceError):
        value.request_id = "other"
    assert not hasattr(value, "__dict__")


def test_binding_revision_must_be_positive_integer():
    value = preparation()
    for revision in (0, True, "1"):
        with pytest.raises((TypeError, ValueError)):
            replace(value.binding, revision=revision)
