from collections.abc import Callable
from typing import Protocol, runtime_checkable

from sp001.contracts.case_access_issuance_completion import (
    CaseAccessIssuanceCompletion,
)
from sp001.contracts.case_access_issuance_preparation import (
    CaseAccessIssuancePreparation,
)
from sp001.contracts.case_access_issuance_policy import CaseAccessIssuancePolicy
from sp001.contracts.case_access_issuance_request import CaseAccessIssuanceRequest
from sp001.contracts.federated_issuance_context import (
    ValidatedFederatedIssuanceContext,
)
from sp001.contracts.protected_case_access_credential import (
    ProtectedCaseAccessCredential,
)


@runtime_checkable
class CaseAccessIssuanceStore(Protocol):
    """Trusted persistence capability over one coherent authority domain.

    Conformance requires behavioral tests, not only matching method names.
    Historical reads do not authorize credential delivery.
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
        ...

    def read_completed(
        self, *, request_id: str,
    ) -> CaseAccessIssuanceCompletion | None:
        ...

    def confirm(
        self, *, preparation: CaseAccessIssuancePreparation,
        protected: ProtectedCaseAccessCredential, clock: Callable[[], int],
        before_commit: Callable[[], None] | None = None,
    ) -> CaseAccessIssuanceCompletion:
        """Atomically admit or recover the first durable completion.

        Require the exact persisted preparation. Evaluate current binding,
        grant revisions, revocation and lifetime under the same transaction.
        Sample time after acquiring transactional authority.
        Run the local before_commit guard before committing.
        On rejection or failure, preserve prior durable state.
        Return only after successful commit; replays revalidate references
        and return the original completion without replacing its envelope.
        Signing and credential recovery do not belong in this transaction.
        """
        ...
