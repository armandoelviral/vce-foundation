from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.case_read_access import (
    AuthenticatedPrincipal,
    CaseReadAuthenticator,
    CaseReadAuthorizer,
)


def test_principal_preserves_issuer_and_subject_exactly():
    principal = AuthenticatedPrincipal(issuer="issuer-A", subject="subscriber-1")
    assert principal.issuer == "issuer-A"
    assert principal.subject == "subscriber-1"
    assert tuple(field.name for field in fields(principal)) == (
        "issuer", "subject",
    )
    assert not hasattr(principal, "__dict__")


@pytest.mark.parametrize("field", ["issuer", "subject"])
@pytest.mark.parametrize("value", [None, 1, True, "", " "])
def test_principal_rejects_invalid_identity_fields(field, value):
    values = {"issuer": "issuer-A", "subject": "subscriber-1"}
    values[field] = value
    with pytest.raises((TypeError, ValueError)):
        AuthenticatedPrincipal(**values)


@pytest.mark.parametrize("field", ["issuer", "subject"])
def test_identity_is_immutable(field):
    principal = AuthenticatedPrincipal(issuer="issuer-A", subject="subscriber-1")
    with pytest.raises(FrozenInstanceError):
        setattr(principal, field, "other")


def test_same_subject_from_different_issuers_is_not_same_identity():
    first = AuthenticatedPrincipal(issuer="issuer-A", subject="subscriber-1")
    second = AuthenticatedPrincipal(issuer="issuer-B", subject="subscriber-1")
    assert first != second


def test_principal_contains_no_credential_or_implicit_permission():
    principal = AuthenticatedPrincipal(issuer="issuer-A", subject="subscriber-1")
    for attribute in (
        "credential", "token", "secret", "roles",
        "case_ids", "authorized", "can_read_case",
    ):
        assert not hasattr(principal, attribute)


def test_authenticator_and_authorizer_are_separate_ports():
    class Authenticator:
        def authenticate(self, *, credential):
            return None

    class Authorizer:
        def can_read_case(self, *, principal, case_id):
            return False

    assert isinstance(Authenticator(), CaseReadAuthenticator)
    assert not isinstance(Authenticator(), CaseReadAuthorizer)
    assert isinstance(Authorizer(), CaseReadAuthorizer)
    assert not isinstance(Authorizer(), CaseReadAuthenticator)
    assert not isinstance(object(), CaseReadAuthenticator)
    assert not isinstance(object(), CaseReadAuthorizer)
