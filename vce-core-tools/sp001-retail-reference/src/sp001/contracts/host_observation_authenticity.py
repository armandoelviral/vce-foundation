"""A6-D2A: host observation authenticity assessment contract.

This contract grants no operational authority.
"""

from dataclasses import dataclass
from enum import StrEnum


class HostAuthenticityStatus(StrEnum):
    AUTHENTICATED = "AUTHENTICATED"
    REJECTED = "REJECTED"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class HostAuthenticityAssessment:
    status: HostAuthenticityStatus

    def __post_init__(self) -> None:
        if type(self.status) is not HostAuthenticityStatus:
            raise TypeError(
                "status must be a HostAuthenticityStatus"
            )
