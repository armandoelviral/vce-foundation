from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_inspection_observation import (
    RetailInspectionObservation,
)
from sp001.contracts.retail_inspection_observation_store import (
    StoredRetailInspectionObservation,
)


def _request_id(value):
    if not isinstance(value, str):
        raise TypeError("request_id must be a string")
    if not value or any(
        char.isspace() or ord(char) < 32 or ord(char) == 127
        for char in value
    ):
        raise ValueError("request_id must contain no whitespace or controls")


@dataclass(frozen=True, slots=True)
class RetailObservationSaveRequest:
    """Caller intent; construction authenticates nobody and writes nothing."""

    request_id: str
    observation: RetailInspectionObservation

    def __post_init__(self):
        _request_id(self.request_id)
        if type(self.observation) is not RetailInspectionObservation:
            raise TypeError("observation must be an inspection observation")


@dataclass(frozen=True, slots=True)
class RetailObservationOperationIdentity:
    """Principal/case/request key within one configured storage namespace.

    Construction does not authenticate the supplied principal.
    """

    principal: AuthenticatedPrincipal
    case_id: str
    request_id: str

    def __post_init__(self):
        if type(self.principal) is not AuthenticatedPrincipal:
            raise TypeError("principal must be an AuthenticatedPrincipal")
        if not isinstance(self.case_id, str):
            raise TypeError("case_id must be a string")
        if not self.case_id.strip():
            raise ValueError("case_id must not be empty")
        _request_id(self.request_id)


class RetailObservationEffectDisposition(StrEnum):
    CREATED = "CREATED"
    REUSED = "REUSED"


@dataclass(frozen=True, slots=True)
class RetailObservationOperationReceipt:
    """Supplied receipt content, not proof of commit or verified authorship.

    CREATED describes insertion by the original operation; REUSED describes
    acceptance of identical preexisting content. Exact retries preserve this
    original disposition. The codec boundary must validate document schema,
    canonical representation, identity and case before persistence/recovery.
    """

    operation: RetailObservationOperationIdentity
    stored_observation: StoredRetailInspectionObservation
    disposition: RetailObservationEffectDisposition

    def __post_init__(self):
        if type(self.operation) is not RetailObservationOperationIdentity:
            raise TypeError("operation must be an operation identity")
        if type(self.stored_observation) is not StoredRetailInspectionObservation:
            raise TypeError("stored_observation must be a stored observation")
        if type(self.disposition) is not RetailObservationEffectDisposition:
            raise TypeError("disposition must be an effect disposition")


class RetailObservationOperationConflict(RuntimeError):
    """The scoped operation identity already represents different intent."""
