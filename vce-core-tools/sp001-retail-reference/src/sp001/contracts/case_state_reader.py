from typing import Protocol, runtime_checkable

from sp001.contracts.case_state_read_result import CaseStateReadResult


@runtime_checkable
class CaseStateReader(Protocol):
    def read(self, *, case_id: str) -> CaseStateReadResult:
        """Read one case with an explicit outcome."""
        ...
