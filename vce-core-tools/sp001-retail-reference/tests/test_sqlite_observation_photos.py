import sqlite3
from contextlib import closing
from hashlib import sha256

import pytest

import test_sqlite_authorized_inspection_observations as setup
from test_sqlite_observation_operations import Backend, Request, environment
from sp001.contracts.retail_observation_operation import (
    RetailObservationOperationConflict,
)
from sp001.infrastructure.sqlite_observation_operations import (
    ObservationOperationIntegrityFailure,
)


# The SQLite adapter stores opaque bytes; image decoding is outside its scope.
PHOTO = b"original photo bytes\\x00\\xff"


def fixture(tmp_path):
    path, backend, writer = environment(tmp_path)
    grants = setup.SqliteCaseAccessGrants(database_path=path)
    setup.grant(grants, writer.principal, setup.READ)
    reader = setup.access(writer.principal, setup.READ)
    return path, backend, writer, reader, Request("PHOTO-REQUEST", setup.observation())


def counts(path):
    with closing(sqlite3.connect(path)) as db:
        return tuple(
            db.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]
            for table in (
                "retail_inspection_observations",
                "retail_observation_operations",
                "retail_observation_photos",
            )
        )


def test_recovers_exact_photo_after_reopening_and_preserves_retry(tmp_path):
    path, backend, writer, reader, request = fixture(tmp_path)
    receipt = backend.save_operation_authorized(
        access=writer, request=request, photo=PHOTO,
    )
    reopened = Backend(
        database_path=path, expected_audience="OBS", clock=lambda: 150,
    )
    assert reopened.recover_operation_authorized(
        access=reader, identity=receipt.operation, include_photo=True,
    ) == (receipt, PHOTO)
    assert reopened.save_operation_authorized(
        access=writer, request=request, photo=PHOTO,
    ) == receipt
    assert counts(path) == (1, 1, 1)
    with closing(sqlite3.connect(path)) as db:
        assert db.execute(
            "SELECT photo_sha256 FROM retail_observation_operations"
        ).fetchone() == (sha256(PHOTO).hexdigest(),)
        item = request.observation
        assert db.execute(
            "SELECT case_id, observation_id, observation_version "
            "FROM retail_observation_photos"
        ).fetchone() == (
            item.case_id, item.observation_id, str(item.observation_version),
        )


@pytest.mark.parametrize("original,retry", [
    (None, PHOTO), (PHOTO, None), (PHOTO, b"different bytes"),
])
def test_changed_photo_intent_conflicts(tmp_path, original, retry):
    path, backend, writer, reader, request = fixture(tmp_path)
    receipt = backend.save_operation_authorized(
        access=writer, request=request, photo=original,
    )
    with pytest.raises(RetailObservationOperationConflict):
        backend.save_operation_authorized(
            access=writer, request=request, photo=retry,
        )
    assert backend.recover_operation_authorized(
        access=reader, identity=receipt.operation, include_photo=True,
    ) == (receipt, original)
    assert counts(path) == (1, 1, int(original is not None))


def test_cannot_attach_photo_to_an_existing_version(tmp_path):
    path, backend, writer, _, request = fixture(tmp_path)
    backend.save_operation_authorized(access=writer, request=request)
    with pytest.raises(setup.Conflict):
        backend.save_operation_authorized(
            access=writer,
            request=Request("ANOTHER-REQUEST", request.observation),
            photo=PHOTO,
        )
    assert counts(path) == (1, 1, 0)


def test_photo_insert_failure_rolls_back_observation_and_receipt(tmp_path):
    path, backend, writer, _, request = fixture(tmp_path)
    with closing(sqlite3.connect(path)) as db:
        db.execute("""
            CREATE TRIGGER reject_photo BEFORE INSERT ON retail_observation_photos
            BEGIN SELECT RAISE(ABORT, 'forced photo failure'); END
        """)
        db.commit()
    with pytest.raises(sqlite3.IntegrityError, match="forced photo failure"):
        backend.save_operation_authorized(
            access=writer, request=request, photo=PHOTO,
        )
    assert counts(path) == (0, 0, 0)


@pytest.mark.parametrize("statement", [
    "UPDATE retail_observation_photos SET content = X'00'",
    "DELETE FROM retail_observation_photos",
])
def test_missing_or_changed_photo_is_an_integrity_failure(tmp_path, statement):
    path, backend, writer, reader, request = fixture(tmp_path)
    receipt = backend.save_operation_authorized(
        access=writer, request=request, photo=PHOTO,
    )
    with closing(sqlite3.connect(path)) as db:
        db.execute(statement)
        db.commit()
    with pytest.raises(ObservationOperationIntegrityFailure):
        backend.recover_operation_authorized(
            access=reader, identity=receipt.operation, include_photo=True,
        )
    # SAVE authority alone cannot read the pair or learn its integrity status.
    with pytest.raises(setup.Denied):
        backend.recover_operation_authorized(
            access=writer, identity=receipt.operation, include_photo=True,
        )


def test_migrates_existing_receipt_without_inventing_a_photo(tmp_path):
    path, backend, writer, reader, request = fixture(tmp_path)
    receipt = backend.save_operation_authorized(access=writer, request=request)
    # Recreate the prior schema while retaining a real observation and receipt.
    with closing(sqlite3.connect(path)) as db:
        db.execute("DROP TABLE retail_observation_photos")
        db.execute(
            "ALTER TABLE retail_observation_operations DROP COLUMN photo_sha256"
        )
        db.commit()
    reopened = Backend(
        database_path=path, expected_audience="OBS", clock=lambda: 150,
    )
    assert reopened.recover_operation_authorized(
        access=reader, identity=receipt.operation, include_photo=True,
    ) == (receipt, None)
    assert counts(path) == (1, 1, 0)
