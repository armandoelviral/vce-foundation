from collections.abc import Callable
import time

from sp001.contracts.federated_issuance_context import (
    ValidatedFederatedIssuanceContext,
)
from sp001.contracts.case_access_issuance_preparation import (
    CaseAccessIssuancePreparation,
)
from sp001.contracts.federated_issuance_authenticator import (
    FederatedIssuanceAuthenticator,
)
from sp001.contracts.case_access_issuance_backend import (
    CaseAccessIssuanceBackend,
)


from sp001.contracts.case_access_issuance_policy import CaseAccessIssuancePolicy
from sp001.contracts.case_access_issuance_request import CaseAccessIssuanceRequest


class IssuanceAuthenticationRejected(PermissionError):
    pass


class IssuanceIdentityRejected(PermissionError):
    pass


class AuthenticatedCaseAccessIssuance:
    """Authenticate each call and bind it to the prepared external identity."""

    def __init__(
        self, *, authenticator: FederatedIssuanceAuthenticator,
        backend: CaseAccessIssuanceBackend,
        expected_audience: str,
        clock: Callable[[], int] | None = None,
        issuance_policy: CaseAccessIssuancePolicy | None = None,
    ):
        if not callable(getattr(authenticator, "authenticate", None)):
            raise TypeError("authenticator must implement authenticate")
        if not isinstance(backend, CaseAccessIssuanceBackend):
            raise TypeError("backend must implement CaseAccessIssuanceBackend")
        if clock is not None and not callable(clock):
            raise TypeError("clock must be callable")
        if not isinstance(expected_audience, str) or not expected_audience.strip():
            raise ValueError('expected_audience must be a nonempty string')
        if issuance_policy is not None:
            if not isinstance(issuance_policy, CaseAccessIssuancePolicy):
                raise TypeError('issuance_policy must be a CaseAccessIssuancePolicy')
            if issuance_policy.primary_audience != expected_audience:
                raise ValueError('policy primary audience must match verifier audience')
        self._issuance_policy = issuance_policy
        self._audience = expected_audience
        self._authenticator = authenticator
        self._backend = backend
        self._clock = clock if clock is not None else lambda: int(time.time())

    def _authenticate(self, credential):
        if not isinstance(credential, str) or not credential.strip():
            raise IssuanceAuthenticationRejected("primary credential rejected")
        context = self._authenticator.authenticate(credential=credential)
        if context is None:
            raise IssuanceAuthenticationRejected("primary credential rejected")
        if not isinstance(context, ValidatedFederatedIssuanceContext):
            raise TypeError("authenticator returned an invalid context")
        self._require_valid(context)
        return context

    def _require_valid(self, context):
        try:
            context.require_valid(
                expected_audience=self._audience, at_time=self._clock(),
            )
        except PermissionError as error:
            raise IssuanceAuthenticationRejected(
                "primary credential audience or lifetime rejected"
            ) from error

    @staticmethod
    def _require_identity(principal, preparation):
        if principal != preparation.binding.external_principal:
            raise IssuanceIdentityRejected("issuance identity rejected")

    def prepare(self, *, credential, preparation):
        context = self._authenticate(credential)
        if not isinstance(preparation, CaseAccessIssuancePreparation):
            raise TypeError("preparation must be a CaseAccessIssuancePreparation")
        self._require_identity(context.principal, preparation)
        return self._backend.prepare(
            preparation=preparation, at_time=self._clock(),
            before_commit=lambda: self._require_valid(context),
        )

    def complete(self, *, credential, request_id):
        context = self._authenticate(credential)
        preparation = self._backend.read_prepared(request_id=request_id)
        if preparation is None:
            raise IssuanceIdentityRejected("issuance identity rejected")
        self._require_identity(context.principal, preparation)
        # Durable completion revalidates binding and grants, including on replay.
        token = self._backend.complete(
            request_id=request_id,
            before_commit=lambda: self._require_valid(context),
        )
        self._require_valid(context)
        return token

    def prepare_request(self, *, credential, request):
        context = self._authenticate(credential)
        if not isinstance(request, CaseAccessIssuanceRequest):
            raise TypeError("request must be a CaseAccessIssuanceRequest")
        if self._issuance_policy is None:
            raise RuntimeError("limited issuance policy is not configured")
        return self._backend.prepare_request(
            request=request, context=context,
            policy=self._issuance_policy, clock=self._clock,
        )
