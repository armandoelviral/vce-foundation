"""Authenticated commercial decision service.

The authenticator is trusted to verify credential authenticity.
This service does not administer grants or verify document provenance.
"""

from collections.abc import Callable

from sp001.contracts.federated_issuance_context import (
    ValidatedFederatedIssuanceContext,
)
from sp001.contracts.product001_commercial_approval_decision import (
    Product001CommercialApprovalDecision,
)


class CommercialAuthenticationRejected(PermissionError):
    pass


class CommercialIdentityRejected(PermissionError):
    pass


class AuthenticatedProduct001CommercialApproval:
    def __init__(
        self, *, authenticator, writer,
        expected_audience: str,
        clock: Callable[[], int],
    ):
        if not callable(getattr(authenticator, "authenticate", None)):
            raise TypeError("authenticator must implement authenticate")
        if not callable(getattr(writer, "save_decision", None)):
            raise TypeError("writer must implement save_decision")
        if (
            not isinstance(expected_audience, str)
            or not expected_audience.strip()
        ):
            raise ValueError("invalid expected audience")
        if not callable(clock):
            raise TypeError("clock must be callable")

        self._authenticator = authenticator
        self._writer = writer
        self._audience = expected_audience
        self._clock = clock

    def _require_valid(self, context):
        try:
            context.require_valid(
                expected_audience=self._audience,
                at_time=self._clock(),
            )
        except PermissionError as exc:
            raise CommercialAuthenticationRejected(
                "credential audience or lifetime rejected"
            ) from exc

    def record(self, *, credential, decision):
        if not isinstance(credential, str) or not credential.strip():
            raise CommercialAuthenticationRejected(
                "credential rejected"
            )
        if not isinstance(
            decision, Product001CommercialApprovalDecision
        ):
            raise TypeError("invalid commercial decision")

        context = self._authenticator.authenticate(
            credential=credential
        )
        if context is None:
            raise CommercialAuthenticationRejected(
                "credential rejected"
            )
        if not isinstance(
            context, ValidatedFederatedIssuanceContext
        ):
            raise TypeError("invalid authenticator result")

        self._require_valid(context)

        if decision.principal != context.principal:
            raise CommercialIdentityRejected(
                "commercial decision principal mismatch"
            )

        return self._writer.save_decision(
            decision=decision,
            authenticated_principal=context.principal,
            before_commit=lambda: self._require_valid(context),
        )
