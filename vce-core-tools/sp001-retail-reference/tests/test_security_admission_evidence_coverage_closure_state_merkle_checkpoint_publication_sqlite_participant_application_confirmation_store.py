import inspect
import json
import sqlite3

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_parsing import (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_sqlite_participant_application_confirmation_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteParticipantApplicationConfirmationStore,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    create_set,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)
ConfirmationStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore
)
SqliteStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteParticipantApplicationConfirmationStore
)

_TABLE_NAME = (
    "security_admission_merkle_checkpoint_publication_"
    "participant_application_confirmations"
)


def confirmation_set(
    *,
    size: int = 3,
    decision: Decision = Decision.COMMIT,
    scalar: int = 1,
) -> ConfirmationSet:
    return create_set(
        size=size,
        decision=decision,
        scalar=scalar,
    )


def create_store(
    tmp_path: Path,
    *,
    name: str = "application-confirmations.sqlite3",
) -> SqliteStore:
    return SqliteStore(
        database_path=tmp_path / name,
    )


def publication_id(
    value: ConfirmationSet,
) -> str:
    assert value.confirmations
    return (
        value.confirmations[0]
        .publication_state
        .publication_intent
        .publication_id
    )


def stored_rows(
    database_path: Path,
    *,
    retained_publication_id: str,
) -> list[tuple[str, str]]:
    with sqlite3.connect(database_path) as connection:
        rows = connection.execute(
            f"""
            SELECT participant_id, confirmation_serialization
            FROM {_TABLE_NAME}
            WHERE publication_id = ?
            ORDER BY participant_id ASC
            """,
            (retained_publication_id,),
        ).fetchall()

    assert all(
        type(row) is tuple
        and len(row) == 2
        and type(row[0]) is str
        and type(row[1]) is str
        for row in rows
    )
    return rows


def replace_serialization(
    database_path: Path,
    *,
    retained_publication_id: str,
    participant_id: str,
    serialization: str,
) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            f"""
            UPDATE {_TABLE_NAME}
            SET confirmation_serialization = ?
            WHERE publication_id = ?
              AND participant_id = ?
            """,
            (
                serialization,
                retained_publication_id,
                participant_id,
            ),
        )


def canonical_document(
    value: dict[str, object],
) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def test_adapter_implements_confirmation_store_protocol(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)

    assert isinstance(
        store,
        ConfirmationStore,
    )


def test_constructor_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(SqliteStore)

    assert tuple(signature.parameters) == (
        "database_path",
    )
    assert (
        signature.parameters["database_path"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert (
        signature.parameters["database_path"].annotation
        == str | Path
    )
    assert signature.return_annotation is None


@pytest.mark.parametrize(
    "invalid_path",
    (
        None,
        1,
        True,
        b"database.sqlite3",
        object(),
    ),
)
def test_database_path_rejects_invalid_type(
    invalid_path: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="database_path must be a string or pathlib.Path",
    ):
        SqliteStore(
            database_path=invalid_path,
        )


def test_database_path_rejects_empty_string() -> None:
    with pytest.raises(
        ValueError,
        match="database_path must not be empty",
    ):
        SqliteStore(
            database_path="",
        )


def test_constructor_creates_database_and_schema(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "schema.sqlite3"

    SqliteStore(
        database_path=database_path,
    )

    assert database_path.is_file()

    with sqlite3.connect(database_path) as connection:
        columns = connection.execute(
            f"PRAGMA table_info({_TABLE_NAME})"
        ).fetchall()

    assert tuple(
        row[1]
        for row in columns
    ) == (
        "publication_id",
        "participant_id",
        "confirmation_serialization",
    )
    assert tuple(
        row[2]
        for row in columns
    ) == (
        "TEXT",
        "TEXT",
        "TEXT",
    )
    assert tuple(
        row[5]
        for row in columns
    ) == (
        1,
        2,
        0,
    )


def test_database_uses_wal_mode(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "wal.sqlite3"

    create_store(
        tmp_path,
        name=database_path.name,
    )

    with sqlite3.connect(database_path) as connection:
        mode = connection.execute(
            "PRAGMA journal_mode"
        ).fetchone()

    assert mode is not None
    assert mode[0].lower() == "wal"


def test_missing_read_returns_empty_canonical_set(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)

    result = store.read(
        publication_id="missing-publication",
    )

    assert result == ConfirmationSet(
        confirmations=(),
    )


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        5,
    ),
)
def test_create_and_read_round_trip_is_exact(
    tmp_path: Path,
    size: int,
) -> None:
    expected = confirmation_set(size=size)
    store = create_store(tmp_path)
    retained_publication_id = publication_id(expected)

    for confirmation in expected.confirmations:
        assert store.create(
            confirmation=confirmation,
        )

    assert store.read(
        publication_id=retained_publication_id,
    ) == expected


def test_abort_confirmations_round_trip_exactly(
    tmp_path: Path,
) -> None:
    expected = confirmation_set(
        size=3,
        decision=Decision.ABORT,
    )
    store = create_store(tmp_path)

    for confirmation in expected.confirmations:
        assert store.create(
            confirmation=confirmation,
        )

    assert store.read(
        publication_id=publication_id(expected),
    ) == expected


def test_reverse_create_order_reads_canonical_order(
    tmp_path: Path,
) -> None:
    expected = confirmation_set(size=5)
    store = create_store(tmp_path)

    for confirmation in reversed(
        expected.confirmations
    ):
        assert store.create(
            confirmation=confirmation,
        )

    result = store.read(
        publication_id=publication_id(expected),
    )

    assert result == expected
    assert tuple(
        confirmation.participant_id
        for confirmation in result.confirmations
    ) == tuple(
        sorted(
            confirmation.participant_id
            for confirmation in result.confirmations
        )
    )


def test_create_persists_canonical_json(
    tmp_path: Path,
) -> None:
    expected = confirmation_set(size=1)
    confirmation = expected.confirmations[0]
    database_path = tmp_path / "canonical.sqlite3"
    store = create_store(
        tmp_path,
        name=database_path.name,
    )

    assert store.create(
        confirmation=confirmation,
    )

    rows = stored_rows(
        database_path,
        retained_publication_id=publication_id(expected),
    )
    assert len(rows) == 1

    serialization = rows[0][1]
    stored = (
        parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
            serialization=serialization,
        )
    )

    assert (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
            stored_confirmation=stored,
        )
        == serialization
    )


def test_duplicate_create_returns_false_and_preserves_original(
    tmp_path: Path,
) -> None:
    expected = confirmation_set(size=1)
    confirmation = expected.confirmations[0]
    store = create_store(tmp_path)

    assert store.create(
        confirmation=confirmation,
    )
    assert not store.create(
        confirmation=confirmation,
    )
    assert store.read(
        publication_id=publication_id(expected),
    ) == expected


def test_distinct_participants_are_independent(
    tmp_path: Path,
) -> None:
    expected = confirmation_set(size=3)
    store = create_store(tmp_path)

    results = tuple(
        store.create(
            confirmation=confirmation,
        )
        for confirmation in expected.confirmations
    )

    assert results == (
        True,
        True,
        True,
    )


def test_confirmations_persist_across_store_instances(
    tmp_path: Path,
) -> None:
    expected = confirmation_set(size=3)
    database_path = tmp_path / "persistent.sqlite3"
    first = create_store(
        tmp_path,
        name=database_path.name,
    )

    for confirmation in expected.confirmations:
        assert first.create(
            confirmation=confirmation,
        )

    second = create_store(
        tmp_path,
        name=database_path.name,
    )

    assert second.read(
        publication_id=publication_id(expected),
    ) == expected


def test_two_concurrent_creators_have_one_winner(
    tmp_path: Path,
) -> None:
    expected = confirmation_set(size=1)
    confirmation = expected.confirmations[0]
    database_path = tmp_path / "concurrent.sqlite3"

    first = create_store(
        tmp_path,
        name=database_path.name,
    )
    second = create_store(
        tmp_path,
        name=database_path.name,
    )

    def create_once(store: SqliteStore) -> bool:
        return store.create(
            confirmation=confirmation,
        )

    with ThreadPoolExecutor(
        max_workers=2,
    ) as executor:
        results = tuple(
            executor.map(
                create_once,
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
    assert first.read(
        publication_id=publication_id(expected),
    ) == expected


@pytest.mark.parametrize(
    "invalid_confirmation",
    (
        None,
        object(),
        "confirmation",
        (),
    ),
)
def test_create_rejects_invalid_confirmation(
    tmp_path: Path,
    invalid_confirmation: object,
) -> None:
    store = create_store(tmp_path)

    with pytest.raises(
        TypeError,
        match="confirmation must be",
    ):
        store.create(
            confirmation=invalid_confirmation,
        )


@pytest.mark.parametrize(
    "invalid_id",
    (
        None,
        1,
        True,
        b"publication",
        object(),
    ),
)
def test_read_rejects_invalid_publication_id_type(
    tmp_path: Path,
    invalid_id: object,
) -> None:
    store = create_store(tmp_path)

    with pytest.raises(
        TypeError,
        match="publication_id must be a string",
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
        match="publication_id must not be empty",
    ):
        store.read(
            publication_id="",
        )


def test_publication_id_is_parameterized_not_executed(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)
    hostile = (
        "publication-001'; DROP TABLE "
        f"{_TABLE_NAME}; --"
    )

    assert store.read(
        publication_id=hostile,
    ) == ConfirmationSet(
        confirmations=(),
    )

    with store._connect() as connection:
        row = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = ?
            """,
            (_TABLE_NAME,),
        ).fetchone()

    assert row == (_TABLE_NAME,)


def test_noncanonical_serialization_fails_closed_on_read(
    tmp_path: Path,
) -> None:
    expected = confirmation_set(size=1)
    confirmation = expected.confirmations[0]
    database_path = tmp_path / "noncanonical.sqlite3"
    store = create_store(
        tmp_path,
        name=database_path.name,
    )

    assert store.create(
        confirmation=confirmation,
    )

    retained_publication_id = publication_id(expected)
    rows = stored_rows(
        database_path,
        retained_publication_id=retained_publication_id,
    )
    document = json.loads(rows[0][1])
    changed = json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
    )
    assert changed != rows[0][1]

    replace_serialization(
        database_path,
        retained_publication_id=retained_publication_id,
        participant_id=confirmation.participant_id,
        serialization=changed,
    )

    with pytest.raises(
        ValueError,
        match="must be canonical",
    ):
        store.read(
            publication_id=retained_publication_id,
        )


def test_changed_stored_participant_id_fails_closed(
    tmp_path: Path,
) -> None:
    expected = confirmation_set(size=1)
    confirmation = expected.confirmations[0]
    database_path = tmp_path / "participant-identity.sqlite3"
    store = create_store(
        tmp_path,
        name=database_path.name,
    )
    assert store.create(
        confirmation=confirmation,
    )

    retained_publication_id = publication_id(expected)
    rows = stored_rows(
        database_path,
        retained_publication_id=retained_publication_id,
    )
    document = json.loads(rows[0][1])
    document["participant_id"] = "different-participant"

    replace_serialization(
        database_path,
        retained_publication_id=retained_publication_id,
        participant_id=confirmation.participant_id,
        serialization=canonical_document(document),
    )

    with pytest.raises(
        ValueError,
        match="different participant_id",
    ):
        store.read(
            publication_id=retained_publication_id,
        )


def test_changed_stored_publication_id_fails_closed(
    tmp_path: Path,
) -> None:
    expected = confirmation_set(size=1)
    confirmation = expected.confirmations[0]
    database_path = tmp_path / "publication-identity.sqlite3"
    store = create_store(
        tmp_path,
        name=database_path.name,
    )
    assert store.create(
        confirmation=confirmation,
    )

    retained_publication_id = publication_id(expected)
    rows = stored_rows(
        database_path,
        retained_publication_id=retained_publication_id,
    )
    document = json.loads(rows[0][1])
    state = document["publication_state"]
    assert isinstance(state, dict)
    state["publication_id"] = "different-publication"

    replace_serialization(
        database_path,
        retained_publication_id=retained_publication_id,
        participant_id=confirmation.participant_id,
        serialization=canonical_document(document),
    )

    with pytest.raises(
        ValueError,
        match="different publication_id",
    ):
        store.read(
            publication_id=retained_publication_id,
        )


def test_conflicting_decisions_fail_closed_on_read(
    tmp_path: Path,
) -> None:
    committed = confirmation_set(
        size=2,
        decision=Decision.COMMIT,
    )
    aborted = confirmation_set(
        size=2,
        decision=Decision.ABORT,
    )
    store = create_store(tmp_path)

    assert store.create(
        confirmation=committed.confirmations[0],
    )
    assert store.create(
        confirmation=aborted.confirmations[1],
    )

    with pytest.raises(
        ValueError,
        match="same publication decision",
    ):
        store.read(
            publication_id=publication_id(committed),
        )


def test_conflicting_signed_intents_fail_closed_on_read(
    tmp_path: Path,
) -> None:
    first = confirmation_set(
        size=2,
        scalar=1,
    )
    second = confirmation_set(
        size=2,
        scalar=2,
    )
    store = create_store(tmp_path)

    assert store.create(
        confirmation=first.confirmations[0],
    )
    assert store.create(
        confirmation=second.confirmations[1],
    )

    with pytest.raises(
        ValueError,
        match="exact same publication intent",
    ):
        store.read(
            publication_id=publication_id(first),
        )


def test_adapter_exposes_no_mutation_after_create() -> None:
    members = set(SqliteStore.__dict__)

    assert members.isdisjoint(
        {
            "update",
            "delete",
            "replace",
            "compare_and_swap",
            "upsert",
        }
    )


def test_adapter_uses_no_pickle() -> None:
    module = inspect.getmodule(SqliteStore)
    assert module is not None

    source = inspect.getsource(module)

    assert "pickle" not in source
    assert "eval(" not in source
    assert "exec(" not in source
