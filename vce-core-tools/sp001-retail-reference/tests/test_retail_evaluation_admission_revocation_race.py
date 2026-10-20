import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from threading import Event, local

import pytest

import test_retail_report_attribution_admission as setup

from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_evaluator_binding_change import (
    RetailEvaluatorBindingChange,
)
from sp001.contracts.retail_evaluation_binding_reference import (
    RetailEvaluationBindingReference,
)
from sp001.services.retail_evaluator_binding_validation import (
    RetailEvaluatorBindingRejected,
)


@pytest.mark.parametrize("first_operation", ["revoke", "admit"])
def test_real_connections_serialize_revocation_and_admission(
    tmp_path, monkeypatch, first_operation,
):
    (
        path, _, principal, report, binding, bindings,
        _, _, auth, _, service,
    ) = setup.environment(tmp_path)

    first_acquired = Event()
    second_attempted = Event()
    release_first = Event()
    role = local()
    real_connect = sqlite3.connect

    class CoordinatedConnection(sqlite3.Connection):
        def execute(self, sql, parameters=()):
            if sql.strip().upper() == "BEGIN IMMEDIATE":
                current_role = getattr(role, "value", None)
                if current_role == "second":
                    second_attempted.set()
                result = super().execute(sql, parameters)
                if current_role == "first":
                    first_acquired.set()
                    if not release_first.wait(timeout=10):
                        raise RuntimeError("test did not release first writer")
                return result
            return super().execute(sql, parameters)

    def connect(*args, **kwargs):
        kwargs["factory"] = CoordinatedConnection
        return real_connect(*args, **kwargs)

    monkeypatch.setattr(sqlite3, "connect", connect)

    revoked = RetailEvaluatorBindingSnapshot(
        binding=replace(binding, revision=2), revoked=True,
    )

    def revoke():
        return bindings.apply(change=RetailEvaluatorBindingChange(
            "RACE-REVOKE", revoked, principal, 150,
        ))

    def admit():
        return setup.save(service, report)

    operations = {"revoke": revoke, "admit": admit}
    second_operation = "admit" if first_operation == "revoke" else "revoke"

    def run(position, operation):
        role.value = position
        try:
            return ("returned", operations[operation]())
        except Exception as error:
            return ("raised", error)
        finally:
            role.value = None

    with ThreadPoolExecutor(max_workers=2) as executor:
        first = executor.submit(run, "first", first_operation)
        second = None
        try:
            assert first_acquired.wait(timeout=10), "first writer did not acquire"
            second = executor.submit(run, "second", second_operation)
            assert second_attempted.wait(timeout=10), "second writer did not attempt"
        finally:
            release_first.set()
        first_result = first.result(timeout=10)
        assert second is not None
        second_result = second.result(timeout=10)

    assert first_result[0] == "returned", first_result
    assert bindings.read_snapshot(binding_id="BINDING") == revoked
    history = bindings.read_history(binding_id="BINDING")
    assert len(history) == 2
    assert history[-1].event_id == "RACE-REVOKE"

    if first_operation == "revoke":
        assert first_result[1] is True
        assert second_result[0] == "raised"
        assert isinstance(second_result[1], RetailEvaluatorBindingRejected)
        assert str(second_result[1]) == "binding_revision_conflict"
        assert setup.counts(path) == (0, 0)

        # Even the current revision cannot admit through a revoked binding.
        with pytest.raises(RetailEvaluatorBindingRejected, match="binding_revoked"):
            setup.save(service, report, references=(
                RetailEvaluationBindingReference("EVAL", "BINDING", 2),
            ))
        assert setup.counts(path) == (0, 0)
        return

    assert first_result[1] == report
    assert second_result == ("returned", True)
    assert setup.counts(path) == (1, 1)

    def persisted_admissions():
        with real_connect(path) as connection:
            return connection.execute(
                "SELECT evaluation_id, document "
                "FROM retail_evaluation_admissions ORDER BY evaluation_id"
            ).fetchall()

    original_admissions = persisted_admissions()
    before = auth.calls

    # Same report retry and new report reuse preserve the original admission.
    assert setup.save(service, report, references=()) == report
    assert setup.save(
        service, report, report_id="REUSED", references=(),
    ) == report
    assert auth.calls == before + 2
    assert persisted_admissions() == original_admissions
    assert setup.counts(path) == (2, 1)

    new_report = replace(report, evaluations=(
        replace(report.evaluations[0], evaluation_id="NEW-EVALUATION"),
    ))
    with pytest.raises(RetailEvaluatorBindingRejected, match="binding_revoked"):
        setup.save(
            service, new_report, report_id="DENIED",
            references=(RetailEvaluationBindingReference(
                "NEW-EVALUATION", "BINDING", 2,
            ),),
        )
    assert persisted_admissions() == original_admissions
    assert setup.counts(path) == (2, 1)

    # Recovery remains authorized independently of the historical binding.
    assert service.recover(
        credential="valid", identity=setup.Identity("REPORT"), case_id="CASE",
    ) == report
