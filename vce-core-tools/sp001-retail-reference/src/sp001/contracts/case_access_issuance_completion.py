from dataclasses import dataclass
from sp001.contracts.protected_case_access_credential import (
    ProtectedCaseAccessCredential,
)


@dataclass(frozen=True, slots=True)
class CaseAccessIssuanceCompletion:
    request_id: str
    completed_at: int
    protected: ProtectedCaseAccessCredential
