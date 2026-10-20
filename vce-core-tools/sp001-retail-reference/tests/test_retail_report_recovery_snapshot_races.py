from concurrent.futures import ThreadPoolExecutor
from threading import Event, local

import pytest

import test_retail_report_attribution_admission as setup

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action, GrantAdministrationRecord,
)
from sp001.services.authenticated_retail_reports import (
    RetailReportAccessDenied, RetailReportAuthenticationRejected,
)


def recover(service):
    return service.recover_with_admissions(
        credential="valid", identity=setup.Identity("REPORT"), case_id="CASE",
    )


@pytest.mark.parametrize("concurrent_change", [
    "admission", "grant_revocation", "expiration",
])
def test_recovery_uses_one_snapshot_but_rechecks_elapsed_validity(
    tmp_path, monkeypatch, concurrent_change,
):
    (
        path, now, principal, report, _, _, grants, definitions,
        _, backend, service,
    ) = setup.environment(tmp_path)

    if concurrent_change == "admission":
        # This report starts with declared attribution only.
        service.save(
            credential="valid", identity=setup.Identity("REPORT"), report=report,
        )
        assert setup.counts(path) == (1, 0)
    else:
        setup.save(service, report)
        assert setup.counts(path) == (1, 1)

    snapshot_established = Event()
    release_reader = Event()
    reader_state = local()
    original_authorize = backend._authorize
    observations = []

    def authorize(connection, access, case_id, *, recover_only=False):
        result = original_authorize(
            connection, access, case_id, recover_only=recover_only,
        )
        if (
            getattr(reader_state, "active", False)
            and not getattr(reader_state, "paused", False)
        ):
            reader_state.paused = True
            assert recover_only
            assert connection.in_transaction
            observations.append("authorized_snapshot_established")
            snapshot_established.set()
            if not release_reader.wait(timeout=10):
                raise RuntimeError("test did not release snapshot reader")
        return result

    monkeypatch.setattr(backend, "_authorize", authorize)

    def read():
        reader_state.active = True
        reader_state.paused = False
        try:
            return recover(service)
        finally:
            reader_state.active = False

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(read)
        try:
            assert snapshot_established.wait(timeout=10)

            if concurrent_change == "admission":
                # Another connection admits the same evaluation in a new report.
                # The older report is not rewritten.
                assert setup.save(
                    service, report, report_id="ADMITTED-LATER",
                ) == report
                assert setup.counts(path) == (2, 1)
            elif concurrent_change == "grant_revocation":
                for index, grant in enumerate(definitions):
                    assert grants.apply(record=GrantAdministrationRecord(
                        f"SNAPSHOT-REVOKE-{index}", principal,
                        Action.REVOKE, grant, 150,
                    ))
                assert setup.counts(path) == (1, 1)
            else:
                now[0] = 300

            # Writes above must finish while the first read remains paused.
            assert not future.done()
        finally:
            release_reader.set()

        if concurrent_change == "expiration":
            with pytest.raises(RetailReportAuthenticationRejected):
                future.result(timeout=10)
            assert setup.counts(path) == (1, 1)
            return

        first = future.result(timeout=10)

    assert observations == ["authorized_snapshot_established"]
    assert first.report == report

    if concurrent_change == "admission":
        assert first.admissions == ()
        assert first.declared_only_evaluation_ids == ("EVAL",)

        second = recover(service)
        assert second.report == report
        assert second.declared_only_evaluation_ids == ()
        assert len(second.admissions) == 1
        assert second.admissions[0].evaluation == report.evaluations[0]
        assert second.admissions[0].binding_snapshot.binding.revision == 1
        assert setup.counts(path) == (2, 1)
    else:
        # The established snapshot permits the current read; a fresh one denies.
        assert len(first.admissions) == 1
        assert first.declared_only_evaluation_ids == ()
        with pytest.raises(RetailReportAccessDenied):
            recover(service)
        assert setup.counts(path) == (1, 1)
