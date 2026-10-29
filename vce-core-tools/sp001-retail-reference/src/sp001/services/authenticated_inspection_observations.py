from collections.abc import Callable
from typing import Protocol, runtime_checkable

from sp001.contracts.case_access_context import (
    CaseAccessContextAuthenticator,
    CaseAccessOperation as Operation,
    ValidatedCaseAccessContext,
)
from sp001.contracts.retail_inspection_observation import (
    RetailInspectionObservation,
)
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationIdentity,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAuthenticationRejected as Rejected,
    InspectionObservationAccessDenied as Denied,
)
from sp001.services.retail_observation_access_policy import (
    required_retail_observation_permissions,
    token_allows_retail_observation,
)


@runtime_checkable
class AuthorizedInspectionObservationBackend(Protocol):
    def save_authorized(
        self, *, access: ValidatedCaseAccessContext,
        observation: RetailInspectionObservation,
    ) -> RetailInspectionObservation:
        """Validate current grants within the write transaction."""
        ...

    def recover_authorized(
        self, *, access: ValidatedCaseAccessContext,
        identity: RetailInspectionObservationIdentity, case_id: str,
    ) -> RetailInspectionObservation | None:
        """Authorize and recover from one snapshot; verify case and key."""
        ...


class AuthenticatedInspectionObservations:
    """Authenticate every request to an explicitly authorized backend.

    Does not verify the identity of the declared observer or grant authority
    to approve, evaluate or close. Backend failures propagate.
    A save error can leave commit outcome unknown.
    """

    def __init__(
        self, *, authenticator: CaseAccessContextAuthenticator,
        backend: AuthorizedInspectionObservationBackend,
        expected_audience: str, clock: Callable[[], int],
    ) -> None:
        if not isinstance(authenticator, CaseAccessContextAuthenticator):
            raise TypeError("invalid authenticator")
        if not isinstance(backend, AuthorizedInspectionObservationBackend):
            raise TypeError("invalid authorized backend")
        if not isinstance(expected_audience, str):
            raise TypeError("expected_audience must be a string")
        if not expected_audience.strip():
            raise ValueError("expected_audience must not be empty")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._authenticator = authenticator
        self._backend = backend
        self._audience = expected_audience
        self._clock = clock

    def _authenticate(self, credential):
        if not isinstance(credential, str):
            raise TypeError("credential must be a string")
        access = self._authenticator.authenticate(credential=credential)
        if access is None:
            raise Rejected("credential rejected")
        if not isinstance(access, ValidatedCaseAccessContext):
            raise TypeError("authenticator returned an invalid context")
        return access

    def _check(self, access, case_id, operation):
        now = self._clock()
        if type(now) is not int:
            raise TypeError("clock must return integer Unix seconds")
        if now < 0:
            raise ValueError("clock must return nonnegative Unix seconds")
        if (
            access.audience != self._audience
            or not access.issued_at <= access.not_before <= now < access.expires_at
        ):
            raise Rejected("access context unusable")
        if not token_allows_retail_observation(
            access=access, case_id=case_id, operation=operation,
            expected_audience=self._audience, at_time=now,
        ):
            raise Denied("observation access denied")

    def save(self, *, credential, observation):
        if type(observation) is not RetailInspectionObservation:
            raise TypeError("observation must be a RetailInspectionObservation")
        access = self._authenticate(credential)
        self._check(access, observation.case_id, Operation.SAVE_RETAIL_OBSERVATION)
        result = self._backend.save_authorized(
            access=access, observation=observation,
        )
        self._check(access, observation.case_id, Operation.SAVE_RETAIL_OBSERVATION)
        if type(result) is not RetailInspectionObservation:
            raise TypeError("backend returned an invalid observation")
        if result != observation:
            raise ValueError("backend returned a different observation")
        return result

    def recover(self, *, credential, identity, case_id):
        if type(identity) is not RetailInspectionObservationIdentity:
            raise TypeError("identity must be an observation identity")
        required_retail_observation_permissions(
            case_id=case_id, operation=Operation.READ_RETAIL_OBSERVATION,
        )
        access = self._authenticate(credential)
        self._check(access, case_id, Operation.READ_RETAIL_OBSERVATION)
        result = self._backend.recover_authorized(
            access=access, identity=identity, case_id=case_id,
        )
        self._check(access, case_id, Operation.READ_RETAIL_OBSERVATION)
        if result is None:
            return None
        if type(result) is not RetailInspectionObservation:
            raise TypeError("backend returned an invalid observation")
        if result.case_id != case_id:
            raise Denied("observation access denied")
        if (
            result.observation_id != identity.observation_id
            or result.observation_version != identity.observation_version
        ):
            raise ValueError("backend returned a different observation identity")
        return result
