from dataclasses import dataclass

from sp001.contracts.case_access_context import (
    CaseAccessOperation, CaseAccessPermission,
)


@dataclass(frozen=True, slots=True)
class CaseAccessIssuanceRequest:
    """Caller intent only; conveys no identity or authorization."""

    request_id: str
    case_id: str
    operation: CaseAccessOperation

    def __post_init__(self):
        if not isinstance(self.request_id, str):
            raise TypeError("request_id must be a string")
        if (
            not self.request_id.strip()
            or any(character.isspace() or ord(character) < 32
                   or ord(character) == 127 for character in self.request_id)
        ):
            raise ValueError("request_id must contain no whitespace or controls")
        if not isinstance(self.operation, CaseAccessOperation):
            raise TypeError("operation must be a CaseAccessOperation")
        CaseAccessPermission(case_id=self.case_id, operation=self.operation)

    @property
    def permission(self) -> CaseAccessPermission:
        return CaseAccessPermission(
            case_id=self.case_id, operation=self.operation,
        )


class IssuanceRequestConflictError(ValueError):
    """An existing request identifier describes different issuance intent."""
