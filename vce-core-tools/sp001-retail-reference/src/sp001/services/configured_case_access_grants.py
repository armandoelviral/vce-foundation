import time

from sp001.contracts.case_access_grant import (
    CaseAccessGrant,
    CaseAccessGrantSource,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import (
    CaseAccessOperation,
    CaseAccessPermission,
    ValidatedCaseAccessContext,
)


class ConfiguredCaseAccessGrants:
    """Immutable configured snapshot; absent or expired grants deny access."""

    def __init__(self, *, grants: tuple[CaseAccessGrant, ...]) -> None:
        if not isinstance(grants, tuple):
            raise TypeError("grants must be a tuple")
        if any(not isinstance(grant, CaseAccessGrant) for grant in grants):
            raise TypeError("grants must contain CaseAccessGrant")
        identifiers = [grant.grant_id for grant in grants]
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("grant identifiers must be unique")
        self._grants = grants

    def permits(
        self,
        *,
        principal: AuthenticatedPrincipal,
        permission: CaseAccessPermission,
        at_time: int,
    ) -> bool:
        if not isinstance(principal, AuthenticatedPrincipal):
            raise TypeError("principal must be an AuthenticatedPrincipal")
        if not isinstance(permission, CaseAccessPermission):
            raise TypeError("permission must be a CaseAccessPermission")
        if isinstance(at_time, bool) or not isinstance(at_time, int):
            raise TypeError("at_time must be integer Unix seconds")
        if at_time < 0:
            raise ValueError("at_time must not be negative")
        return any(
            grant.principal == principal
            and grant.permission == permission
            and grant.valid_from <= at_time < grant.expires_at
            for grant in self._grants
        )


class GrantBackedCaseReadAuthorizer:
    """Require both a token permission and a currently effective grant."""

    def __init__(self, *, grants: CaseAccessGrantSource) -> None:
        if not isinstance(grants, CaseAccessGrantSource):
            raise TypeError("grants must implement CaseAccessGrantSource")
        self._grants = grants

    def can_read_case(
        self, *, access: ValidatedCaseAccessContext, case_id: str
    ) -> bool:
        if not isinstance(access, ValidatedCaseAccessContext):
            raise TypeError("access must be a ValidatedCaseAccessContext")
        permission = CaseAccessPermission(case_id, CaseAccessOperation.READ_STATE)
        now = int(time.time())
        if not access.issued_at <= access.not_before <= now < access.expires_at:
            return False
        if permission not in access.permissions:
            return False
        decision = self._grants.permits(
            principal=access.principal, permission=permission, at_time=now
        )
        if type(decision) is not bool:
            raise TypeError("grant source must return an exact bool")
        return decision
