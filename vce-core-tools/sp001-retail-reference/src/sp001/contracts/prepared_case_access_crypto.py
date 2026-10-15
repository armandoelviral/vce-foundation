from typing import Protocol, runtime_checkable

from sp001.contracts.case_access_issuance_preparation import (
    CaseAccessIssuancePreparation,
)
from sp001.contracts.case_access_token_issuance import IssuedCaseAccessToken
from sp001.contracts.protected_case_access_credential import (
    ProtectedCaseAccessCredential,
)


@runtime_checkable
class PreparedAccessTokenSigner(Protocol):
    """Trusted signer of exact prepared claims and configured signing identity."""

    def sign(
        self, *, preparation: CaseAccessIssuancePreparation,
    ) -> IssuedCaseAccessToken:
        ...


@runtime_checkable
class PreparedAccessCredentialProtector(Protocol):
    """Authenticated protection bound to the complete preparation.

    Implementations must reject tampering and use with another preparation.
    This port currently uses the persisted credential envelope profile.
    """

    def protect(
        self, *, preparation: CaseAccessIssuancePreparation,
        token: IssuedCaseAccessToken,
    ) -> ProtectedCaseAccessCredential:
        ...

    def recover(
        self, *, preparation: CaseAccessIssuancePreparation,
        protected: ProtectedCaseAccessCredential,
    ) -> IssuedCaseAccessToken:
        ...
