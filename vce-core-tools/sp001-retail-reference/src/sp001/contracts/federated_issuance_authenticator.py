from typing import Protocol

from sp001.contracts.federated_issuance_context import (
    ValidatedFederatedIssuanceContext,
)


class FederatedIssuanceAuthenticator(Protocol):
    """Verify the primary credential for this issuance service.

    Implementations validate signature, trusted issuer, audience and lifetime.
    Invalid credentials return None; provider failures propagate separately.
    """

    def authenticate(
        self, *, credential: str,
    ) -> ValidatedFederatedIssuanceContext | None: ...
