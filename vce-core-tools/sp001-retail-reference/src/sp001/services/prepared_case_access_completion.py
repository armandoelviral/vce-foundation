from collections.abc import Callable
import time

from sp001.contracts.case_access_issuance_store import CaseAccessIssuanceStore
from sp001.contracts.case_access_token_issuance import IssuedCaseAccessToken
from sp001.contracts.prepared_case_access_crypto import (
    PreparedAccessTokenSigner, PreparedAccessCredentialProtector,
)
from sp001.contracts.protected_case_access_credential import (
    ProtectedCaseAccessCredential,
)


class PreparedCaseAccessCompleter:
    """Internal issuance capability: sign, protect, confirm, then release."""

    def __init__(
        self, *, store: CaseAccessIssuanceStore,
        signer: PreparedAccessTokenSigner,
        protector: PreparedAccessCredentialProtector,
        clock: Callable[[], int] | None = None,
    ):
        if not isinstance(store, CaseAccessIssuanceStore):
            raise TypeError("store must implement CaseAccessIssuanceStore")
        if not isinstance(signer, PreparedAccessTokenSigner):
            raise TypeError("signer must implement PreparedAccessTokenSigner")
        if not isinstance(protector, PreparedAccessCredentialProtector):
            raise TypeError("protector must implement PreparedAccessCredentialProtector")
        if clock is not None and not callable(clock):
            raise TypeError("clock must be callable")
        self._store = store
        self._signer = signer
        self._protector = protector
        self._clock = clock if clock is not None else lambda: int(time.time())

    def complete(self, *, request_id: str, before_commit=None) -> IssuedCaseAccessToken:
        preparation = self._store.read_prepared(request_id=request_id)
        if preparation is None:
            raise ValueError("persisted preparation is required")
        historical = self._store.read_completed(request_id=request_id)
        if historical is None:
            token = self._signer.sign(preparation=preparation)
            if not isinstance(token, IssuedCaseAccessToken):
                raise TypeError("signer returned an invalid token")
            protected = self._protector.protect(
                preparation=preparation, token=token,
            )
        else:
            protected = historical.protected

        if not isinstance(protected, ProtectedCaseAccessCredential):
            raise TypeError("protector returned an invalid envelope")

        # Replays also revalidate current references. First completion wins.
        persisted = self._store.confirm(
            preparation=preparation, protected=protected, clock=self._clock,
            before_commit=before_commit,
        )
        recovered = self._protector.recover(
            preparation=preparation, protected=persisted.protected,
        )
        if not isinstance(recovered, IssuedCaseAccessToken):
            raise TypeError("protector returned an invalid token")
        return recovered

    def prepare(self, *, preparation, at_time, before_commit=None):
        return self._store.prepare(
            preparation=preparation, at_time=at_time,
            before_commit=before_commit,
        )

    def prepare_request(self, *, request, context, policy, clock):
        return self._store.prepare_request(
            request=request, context=context, policy=policy, clock=clock,
        )

    def read_prepared(self, *, request_id):
        return self._store.read_prepared(request_id=request_id)
