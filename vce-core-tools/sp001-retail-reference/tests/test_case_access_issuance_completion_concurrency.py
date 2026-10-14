import sqlite3
import threading

from test_case_access_issuance_completion import components
from sp001.infrastructure import sqlite_case_access_issuance_preparations as module


def test_completion_blocks_writer_after_reference_validation(
    components, monkeypatch,
):
    path, store, _, _, preparation, _, _, completer = components
    validated = threading.Event()
    attempted = threading.Event()
    outcomes = []
    errors = []
    original = module.validate_issuance_references

    def competing_writer():
        try:
            assert validated.wait(timeout=5)
            with sqlite3.connect(path, timeout=0) as connection:
                try:
                    connection.execute("BEGIN IMMEDIATE")
                except sqlite3.OperationalError as error:
                    assert error.sqlite_errorcode == sqlite3.SQLITE_BUSY
                    outcomes.append("blocked")
                else:
                    connection.rollback()
                    raise AssertionError("writer acquired the completion lock")
        except BaseException as error:
            errors.append(error)
        finally:
            attempted.set()

    def validate_then_pause(**kwargs):
        original(**kwargs)
        validated.set()
        assert attempted.wait(timeout=5)
        assert errors == []
        assert outcomes == ["blocked"]

    monkeypatch.setattr(
        module, "validate_issuance_references", validate_then_pause,
    )
    thread = threading.Thread(target=competing_writer, daemon=True)
    thread.start()
    try:
        token = completer.complete(request_id=preparation.request_id)
    finally:
        validated.set()
        thread.join(timeout=5)

    assert not thread.is_alive()
    assert errors == []
    assert outcomes == ["blocked"]
    assert token.credential
    assert store.read_completed(request_id=preparation.request_id) is not None
