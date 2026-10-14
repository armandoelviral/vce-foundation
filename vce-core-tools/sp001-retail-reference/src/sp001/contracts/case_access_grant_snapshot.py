from dataclasses import dataclass

from sp001.contracts.case_access_grant import CaseAccessGrant


@dataclass(frozen=True, slots=True)
class CaseAccessGrantSnapshot:
    """Grant and administrative revision read from one persistent snapshot."""

    grant: CaseAccessGrant
    revision: int
    revoked: bool

    def __post_init__(self) -> None:
        if not isinstance(self.grant, CaseAccessGrant):
            raise TypeError("grant must be a CaseAccessGrant")
        if isinstance(self.revision, bool) or not isinstance(self.revision, int):
            raise TypeError("revision must be an integer")
        if self.revision < 1:
            raise ValueError("revision must be positive")
        if type(self.revoked) is not bool:
            raise TypeError("revoked must be an exact bool")
