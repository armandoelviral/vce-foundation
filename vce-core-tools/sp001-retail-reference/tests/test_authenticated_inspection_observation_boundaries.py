from dataclasses import replace

import pytest

from test_retail_inspection_observation import observation
from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
    CaseAccessPermission,
    ValidatedCaseAccessContext,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationIdentity as Identity,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAuthenticationRejected as Rejected,
    InspectionObservationAccessDenied as Denied,
)
from sp001.services.authenticated_inspection_observations import (
    AuthenticatedInspectionObservations as Service,
)


def context():
    return ValidatedCaseAccessContext(
        AuthenticatedPrincipal("ISSUER", "SUBJECT"), "OBS",
        100, 100, 200,
        tuple(CaseAccessPermission("CASE-1", operation) for operation in (
            Operation.SAVE_RETAIL_OBSERVATION,
            Operation.READ_RETAIL_OBSERVATION,
        )),
    )


class Authenticator:
    def __init__(self, reply, error=None):
        self.reply = reply
        self.error = error
        self.calls = 0

    def authenticate(self, *, credential):
        self.calls += 1
        if self.error is not None:
            raise self.error
        return self.reply


class Backend:
    """Boundary double: does not model storage or local authorization."""

    def __init__(self, reply, error=None):
        self.reply = reply
        self.error = error
        self.calls = []

    def save_authorized(self, *, access, observation):
        self.calls.append(("save", access, observation))
        if self.error is not None:
            raise self.error
        return self.reply

    def recover_authorized(self, *, access, identity, case_id):
        self.calls.append(("recover", access, identity, case_id))
        if self.error is not None:
            raise self.error
        return self.reply


def service(auth, backend, clock=lambda: 150):
    return Service(
        authenticator=auth, backend=backend,
        expected_audience="OBS", clock=clock,
    )


def invoke(subject, operation):
    if operation == "save":
        return subject.save(credential="credential", observation=observation())
    return subject.recover(
        credential="credential", identity=Identity("OBS-1", 1),
        case_id="CASE-1",
    )


@pytest.mark.parametrize("operation", ["save", "recover"])
@pytest.mark.parametrize("reply,error", [
    (None, Rejected),
    ("untyped context", TypeError),
])
def test_rejected_or_invalid_authentication_never_calls_backend(
    operation, reply, error,
):
    auth = Authenticator(reply)
    backend = Backend(observation())
    with pytest.raises(error):
        invoke(service(auth, backend), operation)
    assert auth.calls == 1
    assert backend.calls == []


@pytest.mark.parametrize("operation", ["save", "recover"])
def test_authenticator_failure_propagates_without_backend_call(operation):
    failure = OSError("synthetic identity provider failure")
    auth = Authenticator(None, error=failure)
    backend = Backend(observation())
    with pytest.raises(OSError) as caught:
        invoke(service(auth, backend), operation)
    assert caught.value is failure
    assert backend.calls == []


@pytest.mark.parametrize("operation", ["save", "recover"])
@pytest.mark.parametrize("fault,error", [
    ("audience", Rejected),
    ("expired", Rejected),
    ("not_yet_valid", Rejected),
    ("permissions", Denied),
    ("case", Denied),
])
def test_unusable_context_never_calls_backend(operation, fault, error):
    access = context()
    now = 150
    if fault == "audience":
        access = replace(access, audience="OTHER")
    elif fault == "expired":
        now = 200
    elif fault == "not_yet_valid":
        now = 99
    elif fault == "permissions":
        access = replace(access, permissions=())
    else:
        access = replace(access, permissions=tuple(
            replace(permission, case_id="OTHER")
            for permission in access.permissions
        ))
    backend = Backend(observation())
    with pytest.raises(error):
        invoke(service(Authenticator(access), backend, lambda: now), operation)
    assert backend.calls == []


@pytest.mark.parametrize("operation", ["save", "recover"])
@pytest.mark.parametrize("failure", [
    OSError("storage unavailable"),
    Denied("revoked local grant"),
    Rejected("expired in backend"),
])
def test_backend_failure_propagates_without_becoming_absence(operation, failure):
    backend = Backend(None, error=failure)
    with pytest.raises(type(failure)) as caught:
        invoke(service(Authenticator(context()), backend), operation)
    assert caught.value is failure
    assert len(backend.calls) == 1


@pytest.mark.parametrize("operation", ["save", "recover"])
@pytest.mark.parametrize("reply", ["document", object(), {}])
def test_rejects_invalid_backend_return_type(operation, reply):
    with pytest.raises(TypeError):
        invoke(service(Authenticator(context()), Backend(reply)), operation)


def test_none_is_valid_only_for_authorized_recovery():
    auth = Authenticator(context())
    backend = Backend(None)
    subject = service(auth, backend)
    assert invoke(subject, "recover") is None
    with pytest.raises(TypeError):
        invoke(subject, "save")
    assert auth.calls == 2


def test_save_rejects_backend_content_change():
    changed = replace(observation(), description="Unexpected content.")
    with pytest.raises(ValueError, match="different observation"):
        invoke(service(Authenticator(context()), Backend(changed)), "save")


@pytest.mark.parametrize("field,value", [
    ("observation_id", "OTHER"),
    ("observation_version", 2),
])
def test_recovery_rejects_different_exact_identity(field, value):
    changed = replace(observation(), **{field: value})
    with pytest.raises(ValueError, match="different observation identity"):
        invoke(service(Authenticator(context()), Backend(changed)), "recover")


def test_recovery_rejects_other_case():
    changed = replace(observation(), case_id="OTHER")
    with pytest.raises(Denied):
        invoke(service(Authenticator(context()), Backend(changed)), "recover")


@pytest.mark.parametrize("operation", ["save", "recover"])
def test_expiration_after_backend_return_rejects_result(operation):
    times = iter((150, 200))
    backend = Backend(observation())
    subject = service(
        Authenticator(context()), backend, clock=lambda: next(times),
    )
    with pytest.raises(Rejected):
        invoke(subject, operation)
    assert len(backend.calls) == 1
    # This double proves final rejection, not rollback of an actual save.


def test_expiration_also_rejects_absence_response():
    times = iter((150, 200))
    subject = service(
        Authenticator(context()), Backend(None), clock=lambda: next(times),
    )
    with pytest.raises(Rejected):
        invoke(subject, "recover")


@pytest.mark.parametrize("operation", ["save", "recover"])
def test_passes_exact_authenticated_context_to_backend(operation):
    access = context()
    backend = Backend(observation())
    subject = service(Authenticator(access), backend)
    assert invoke(subject, operation) == observation()
    assert backend.calls[0][1] is access


def test_invalid_public_inputs_do_not_authenticate():
    auth = Authenticator(context())
    backend = Backend(observation())
    subject = service(auth, backend)
    with pytest.raises(TypeError):
        subject.save(credential=None, observation=observation())
    with pytest.raises(TypeError):
        subject.save(credential="credential", observation={})
    with pytest.raises(TypeError):
        subject.recover(
            credential="credential", identity="OBS-1", case_id="CASE-1",
        )
    with pytest.raises(ValueError):
        subject.recover(
            credential="credential", identity=Identity("OBS-1", 1), case_id=" ",
        )
    assert auth.calls == 0
    assert backend.calls == []


@pytest.mark.parametrize("field,value,error", [
    ("authenticator", object(), TypeError),
    ("backend", object(), TypeError),
    ("expected_audience", None, TypeError),
    ("expected_audience", " ", ValueError),
    ("clock", 150, TypeError),
])
def test_rejects_invalid_composition(field, value, error):
    arguments = dict(
        authenticator=Authenticator(context()), backend=Backend(observation()),
        expected_audience="OBS", clock=lambda: 150,
    )
    arguments[field] = value
    with pytest.raises(error):
        Service(**arguments)


@pytest.mark.parametrize("value,error", [
    (True, TypeError), ("150", TypeError), (-1, ValueError),
])
def test_rejects_invalid_clock_before_backend(value, error):
    backend = Backend(observation())
    with pytest.raises(error):
        invoke(
            service(Authenticator(context()), backend, lambda: value), "save",
        )
    assert backend.calls == []
