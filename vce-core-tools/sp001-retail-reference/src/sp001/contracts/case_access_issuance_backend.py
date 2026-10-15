from collections.abc import Callable
from typing import Protocol, runtime_checkable

from sp001.contracts.case_access_issuance_preparation import (
    CaseAccessIssuancePreparation,
)
from sp001.contracts.case_access_issuance_policy import CaseAccessIssuancePolicy
from sp001.contracts.case_access_issuance_request import CaseAccessIssuanceRequest
from sp001.contracts.case_access_token_issuance import IssuedCaseAccessToken
from sp001.contracts.federated_issuance_context import (
    ValidatedFederatedIssuanceContext,
)


@runtime_checkable
class CaseAccessIssuanceBackend(Protocol):
    """Trusted internal capability over one coherent issuance store.

    Implementations must preserve atomic reference validation, exact replay
    semantics, signing outside write transactions and release after commit.
    Structural protocol checks alone do not prove those guarantees.
    before_commit is a local validity guard, not an external I/O hook.
    """

    def prepare(
        self, *, preparation: CaseAccessIssuancePreparation, at_time: int,
        before_commit: Callable[[], None] | None = None,
    ) -> CaseAccessIssuancePreparation:
        ...

    def prepare_request(
        self, *, request: CaseAccessIssuanceRequest,
        context: ValidatedFederatedIssuanceContext,
        policy: CaseAccessIssuancePolicy, clock: Callable[[], int],
    ) -> CaseAccessIssuancePreparation:
        ...

    def read_prepared(
        self, *, request_id: str,
    ) -> CaseAccessIssuancePreparation | None:
        """Historical read; does not authorize credential delivery."""
        ...

    def complete(
        self, *, request_id: str,
        before_commit: Callable[[], None] | None = None,
    ) -> IssuedCaseAccessToken:
        """Revalidate current references on completion and recovery."""
        ...
