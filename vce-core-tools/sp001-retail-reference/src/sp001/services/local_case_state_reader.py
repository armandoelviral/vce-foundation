from sp001.contracts.case_state_reader import CaseStateReader
from sp001.contracts.case_authoritative_state_store import (
    CaseAuthoritativeStateStore,
)
from sp001.contracts.case_state_read_result import (
    Found,
    NotFound,
)
from sp001.services.case_authoritative_state_reading import (
    read_case_authoritative_state,
)


class LocalCaseStateReader:
    """Adapt successful local reads; propagate local failures unchanged."""

    def __init__(self, *, store: CaseAuthoritativeStateStore) -> None:
        if not isinstance(store, CaseAuthoritativeStateStore):
            raise TypeError("store must implement CaseAuthoritativeStateStore")
        self._store = store

    def read(self, *, case_id: str) -> Found | NotFound:
        state = read_case_authoritative_state(
            store=self._store, case_id=case_id
        )
        if state is None:
            return NotFound(case_id=case_id)
        return Found(state=state)
