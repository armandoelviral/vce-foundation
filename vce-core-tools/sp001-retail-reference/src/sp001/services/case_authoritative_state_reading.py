from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_authoritative_state_store import CaseAuthoritativeStateStore


def read_case_authoritative_state(
    *,
    store: CaseAuthoritativeStateStore,
    case_id: str,
) -> CaseAuthoritativeState | None:
    if not isinstance(store, CaseAuthoritativeStateStore):
        raise TypeError("store must implement CaseAuthoritativeStateStore")
    if not isinstance(case_id, str):
        raise TypeError("case_id must be a string")
    if not case_id.strip():
        raise ValueError("case_id must not be empty")

    state = store.read(case_id=case_id)
    if state is not None and not isinstance(state, CaseAuthoritativeState):
        raise TypeError("store.read must return CaseAuthoritativeState or None")
    if state is not None and state.case_id != case_id:
        raise ValueError("store.read returned a different case_id")
    return state
