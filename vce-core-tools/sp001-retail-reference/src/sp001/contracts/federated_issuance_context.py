from dataclasses import dataclass

from sp001.contracts.case_read_access import AuthenticatedPrincipal


@dataclass(frozen=True, slots=True)
class ValidatedFederatedIssuanceContext:
    """Verified credential facts supplied by a trusted authenticator."""

    principal: AuthenticatedPrincipal
    audience: str
    issued_at: int
    not_before: int
    expires_at: int

    def __post_init__(self):
        if not isinstance(self.principal, AuthenticatedPrincipal):
            raise TypeError("principal must be an AuthenticatedPrincipal")
        if not isinstance(self.audience, str) or not self.audience.strip():
            raise ValueError("audience must be a nonempty string")
        for name in ("issued_at", "not_before", "expires_at"):
            value = getattr(self, name)
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer")
        if not self.issued_at <= self.not_before < self.expires_at:
            raise ValueError("invalid credential validity interval")

    def require_valid(self, *, expected_audience: str, at_time: int) -> None:
        if not isinstance(expected_audience, str) or not expected_audience.strip():
            raise ValueError("expected_audience must be a nonempty string")
        if type(at_time) is not int or at_time < 0:
            raise ValueError("at_time must be a nonnegative integer")
        if self.audience != expected_audience:
            raise PermissionError("primary credential audience rejected")
        if not self.not_before <= at_time < self.expires_at:
            raise PermissionError("primary credential lifetime rejected")
