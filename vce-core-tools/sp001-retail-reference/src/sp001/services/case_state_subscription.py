from sp001.services.case_state_reconciliation import (
    CaseStateReconciler,
    CaseView,
)
from sp001.contracts.case_state_reader import CaseStateReader


class CaseStateSubscription:
    """Caller-driven session; no polling, retries or background worker."""

    def __init__(self, *, reader: CaseStateReader, case_id: str) -> None:
        if not isinstance(reader, CaseStateReader):
            raise TypeError("reader must implement CaseStateReader")
        self._reader = reader
        self._reconciler = CaseStateReconciler(case_id=case_id)

    @property
    def view(self) -> CaseView:
        return self._reconciler.view

    def refresh(self) -> CaseView:
        request = self._reconciler.begin_read()
        try:
            result = self._reader.read(case_id=request.case_id)
        except Exception:
            # Cleanup only: do not classify storage/programming failures
            # as transport errors or domain absence.
            self._reconciler.fail_read(request=request)
            raise
        self._reconciler.accept(request=request, result=result)
        return self._reconciler.view
