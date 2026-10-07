import inspect
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_projection import (
    zero_preparation_abort,
)

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_sqlite_decision_evidence_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_deserialization import (
    project_abort_with_incomplete_preparations,
    project_commit,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    create_set as create_participant_set,
)


_TABLE_NAME = (
    "security_admission_merkle_checkpoint_publication_decision_evidence"
)


def commit_record(
    *,
    size: int = 3,
):
    return project_commit(
        size=size,
    )[0]


def abort_record():
    return project_abort_with_incomplete_preparations()[0]


def create_store(
    tmp_path: Path,
    *,
    decision_record=None,
    name: str = "publication-decisions.sqlite3",
):
    if decision_record is None:
        decision_record = commit_record()

    return (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
            database_path=tmp_path / name,
            participant_set=decision_record.participant_set,
        )
    )


def stored_serialization(
    database_path: Path,
    *,
    publication_id: str = "publication-001",
) -> str:
    with sqlite3.connect(database_path) as connection:
        row = connection.execute(
            f"""
            SELECT evidence_serialization
            FROM {_TABLE_NAME}
            WHERE publication_id = ?
            """,
            (publication_id,),
        ).fetchone()

    assert row is not None
    assert type(row[0]) is str
    return row[0]


def replace_serialization(
    database_path: Path,
    *,
    serialization: str,
    publication_id: str = "publication-001",
) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            f"""
            UPDATE {_TABLE_NAME}
            SET evidence_serialization = ?
            WHERE publication_id = ?
            """,
            (
                serialization,
                publication_id,
            ),
        )


def test_adapter_implements_decision_record_store_protocol(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)

    assert isinstance(
        store,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore,
    )


def test_constructor_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore
    )

    assert tuple(signature.parameters) == (
        "database_path",
        "participant_set",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )


@pytest.mark.parametrize(
    "invalid_path",
    (
        None,
        object(),
        1,
        True,
        b"database.sqlite3",
        (),
    ),
)
def test_database_path_rejects_invalid_type(
    invalid_path: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="database_path",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
            database_path=invalid_path,
            participant_set=commit_record().participant_set,
        )


def test_database_path_rejects_empty_string() -> None:
    with pytest.raises(
        ValueError,
        match="database_path",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
            database_path="",
            participant_set=commit_record().participant_set,
        )


@pytest.mark.parametrize(
    "invalid_participant_set",
    (
        None,
        object(),
        "participants",
        (),
        1,
        True,
    ),
)
def test_participant_set_rejects_invalid_type(
    tmp_path: Path,
    invalid_participant_set: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="participant_set",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
            database_path=tmp_path / "invalid.sqlite3",
            participant_set=invalid_participant_set,
        )


def test_constructor_creates_database_and_schema(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "decisions.sqlite3"

    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
        database_path=database_path,
        participant_set=commit_record().participant_set,
    )

    assert database_path.is_file()

    with sqlite3.connect(database_path) as connection:
        row = connection.execute(
            """
            SELECT sql
            FROM sqlite_master
            WHERE type = 'table'
              AND name = ?
            """,
            (_TABLE_NAME,),
        ).fetchone()

    assert row is not None
    assert "publication_id TEXT PRIMARY KEY" in row[0]
    assert "evidence_serialization TEXT NOT NULL" in row[0]
    assert "STRICT" in row[0]


def test_database_uses_wal_mode(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "wal.sqlite3"
    create_store(
        tmp_path,
        name=database_path.name,
    )

    with sqlite3.connect(database_path) as connection:
        journal_mode = connection.execute(
            "PRAGMA journal_mode"
        ).fetchone()[0]

    assert journal_mode == "wal"


def test_missing_read_returns_none(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)

    assert (
        store.read(
            publication_id="missing-publication",
        )
        is None
    )


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        5,
    ),
)
def test_commit_create_and_read_round_trip_is_exact(
    tmp_path: Path,
    size: int,
) -> None:
    decision_record = commit_record(
        size=size,
    )
    store = create_store(
        tmp_path,
        decision_record=decision_record,
    )

    assert store.create(
        decision_record=decision_record,
    )
    assert (
        store.read(
            publication_id=(
                decision_record
                .publication_intent
                .publication_id
            ),
        )
        == decision_record
    )


def test_abort_create_and_read_round_trip_is_exact(
    tmp_path: Path,
) -> None:
    decision_record = abort_record()
    store = create_store(
        tmp_path,
        decision_record=decision_record,
    )

    assert store.create(
        decision_record=decision_record,
    )
    assert (
        store.read(
            publication_id=(
                decision_record
                .publication_intent
                .publication_id
            ),
        )
        == decision_record
    )


def test_create_persists_canonical_json(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "canonical.sqlite3"
    decision_record = commit_record()
    store = create_store(
        tmp_path,
        decision_record=decision_record,
        name=database_path.name,
    )

    assert store.create(
        decision_record=decision_record,
    )

    serialization = stored_serialization(
        database_path,
    )
    assert serialization == json.dumps(
        json.loads(serialization),
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def test_duplicate_create_returns_false_and_preserves_original(
    tmp_path: Path,
) -> None:
    original = commit_record()
    conflicting = abort_record()
    store = create_store(
        tmp_path,
        decision_record=original,
    )

    assert store.create(
        decision_record=original,
    )
    assert not store.create(
        decision_record=conflicting,
    )
    assert (
        store.read(
            publication_id="publication-001",
        )
        == original
    )


def test_record_persists_across_store_instances(
    tmp_path: Path,
) -> None:
    decision_record = commit_record()
    database_path = tmp_path / "persistent.sqlite3"
    first = create_store(
        tmp_path,
        decision_record=decision_record,
        name=database_path.name,
    )

    assert first.create(
        decision_record=decision_record,
    )

    second = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
            database_path=database_path,
            participant_set=decision_record.participant_set,
        )
    )

    assert (
        second.read(
            publication_id="publication-001",
        )
        == decision_record
    )


def test_two_concurrent_creators_have_one_winner(
    tmp_path: Path,
) -> None:
    decision_record = commit_record()
    database_path = tmp_path / "concurrent.sqlite3"
    first = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
            database_path=database_path,
            participant_set=decision_record.participant_set,
        )
    )
    second = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
            database_path=database_path,
            participant_set=decision_record.participant_set,
        )
    )

    with ThreadPoolExecutor(
        max_workers=2,
    ) as executor:
        results = tuple(
            executor.map(
                lambda store: store.create(
                    decision_record=decision_record,
                ),
                (
                    first,
                    second,
                ),
            )
        )

    assert sorted(results) == [
        False,
        True,
    ]
    assert (
        first.read(
            publication_id="publication-001",
        )
        == decision_record
    )


@pytest.mark.parametrize(
    "invalid_record",
    (
        None,
        object(),
        "decision",
        (),
        1,
        True,
    ),
)
def test_create_rejects_invalid_decision_record(
    tmp_path: Path,
    invalid_record: object,
) -> None:
    store = create_store(tmp_path)

    with pytest.raises(
        TypeError,
        match="decision_record",
    ):
        store.create(
            decision_record=invalid_record,
        )


@pytest.mark.parametrize(
    "invalid_id",
    (
        None,
        object(),
        b"publication-001",
        (),
        1,
        True,
    ),
)
def test_read_rejects_invalid_publication_id_type(
    tmp_path: Path,
    invalid_id: object,
) -> None:
    store = create_store(tmp_path)

    with pytest.raises(
        TypeError,
        match="publication_id",
    ):
        store.read(
            publication_id=invalid_id,
        )


def test_read_rejects_empty_publication_id(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)

    with pytest.raises(
        ValueError,
        match="publication_id",
    ):
        store.read(
            publication_id="",
        )


def test_publication_id_is_parameterized_not_executed(
    tmp_path: Path,
) -> None:
    decision_record = commit_record()
    store = create_store(
        tmp_path,
        decision_record=decision_record,
    )

    assert store.create(
        decision_record=decision_record,
    )
    assert (
        store.read(
            publication_id=(
                "publication-001' OR 1=1 --"
            ),
        )
        is None
    )
    assert (
        store.read(
            publication_id="publication-001",
        )
        == decision_record
    )


def test_noncanonical_serialization_fails_closed_on_read(
    tmp_path: Path,
) -> None:
    decision_record = commit_record()
    database_path = tmp_path / "noncanonical.sqlite3"
    store = create_store(
        tmp_path,
        decision_record=decision_record,
        name=database_path.name,
    )
    assert store.create(
        decision_record=decision_record,
    )

    serialization = stored_serialization(
        database_path,
    )
    replace_serialization(
        database_path,
        serialization=" " + serialization,
    )

    with pytest.raises(ValueError):
        store.read(
            publication_id="publication-001",
        )


def test_contradictory_stored_decision_fails_closed_on_read(
    tmp_path: Path,
) -> None:
    decision_record = commit_record()
    database_path = tmp_path / "contradictory.sqlite3"
    store = create_store(
        tmp_path,
        decision_record=decision_record,
        name=database_path.name,
    )
    assert store.create(
        decision_record=decision_record,
    )

    document = json.loads(
        stored_serialization(database_path)
    )
    document["decision"] = "ABORT"
    changed = json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    replace_serialization(
        database_path,
        serialization=changed,
    )

    with pytest.raises(ValueError):
        store.read(
            publication_id="publication-001",
        )


def test_different_provisioned_roster_fails_closed_on_read(
    tmp_path: Path,
) -> None:
    decision_record = commit_record(
        size=3,
    )
    database_path = tmp_path / "roster.sqlite3"
    writer = create_store(
        tmp_path,
        decision_record=decision_record,
        name=database_path.name,
    )
    assert writer.create(
        decision_record=decision_record,
    )

    reader = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore(
            database_path=database_path,
            participant_set=create_participant_set(
                size=2,
            ),
        )
    )

    with pytest.raises(ValueError):
        reader.read(
            publication_id="publication-001",
        )


def test_changed_stored_publication_id_fails_closed(
    tmp_path: Path,
) -> None:
    decision_record = commit_record()
    database_path = tmp_path / "identity.sqlite3"
    store = create_store(
        tmp_path,
        decision_record=decision_record,
        name=database_path.name,
    )
    assert store.create(
        decision_record=decision_record,
    )

    document = json.loads(
        stored_serialization(database_path)
    )
    document["decision_record"][
        "publication_id"
    ] = "different-publication"
    changed = json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    replace_serialization(
        database_path,
        serialization=changed,
    )

    with pytest.raises(
        ValueError,
        match="recorded publication_id",
    ):
        store.read(
            publication_id="publication-001",
        )


def test_adapter_exposes_no_mutation_after_create() -> None:
    adapter = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore
    )

    assert not hasattr(adapter, "update")
    assert not hasattr(adapter, "compare_and_swap")
    assert not hasattr(adapter, "delete")


def test_adapter_uses_no_pickle() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore
    )

    assert "pickle" not in source
    assert "eval(" not in source
    assert "exec(" not in source


def test_zero_preparation_abort_round_trip_is_exact(
    tmp_path: Path,
) -> None:
    decision_record = zero_preparation_abort()
    store = create_store(
        tmp_path,
        decision_record=decision_record,
        name="zero-preparation-abort.sqlite3",
    )

    assert store.create(
        decision_record=decision_record,
    )
    assert (
        store.read(
            publication_id=(
                decision_record
                .publication_intent
                .publication_id
            ),
        )
        == decision_record
    )
