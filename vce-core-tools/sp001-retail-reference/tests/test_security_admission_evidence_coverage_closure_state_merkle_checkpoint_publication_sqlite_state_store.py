import inspect
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_sqlite_state_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteStateStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition import (
    transition_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition_application import (
    apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    create_state,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
SqliteStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteStateStore
)
StateStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore
)
transition = (
    transition_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication
)
apply_transition = (
    apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition
)

UINT64_MAX = (1 << 64) - 1
TABLE = "security_admission_checkpoint_publication_state"


def create_store(
    tmp_path: Path,
    *,
    name: str = "publication.sqlite3",
) -> SqliteStore:
    return SqliteStore(
        database_path=tmp_path / name,
    )


def test_adapter_implements_state_store_protocol(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)

    assert isinstance(store, StateStore)


def test_constructor_has_keyword_only_database_path() -> None:
    signature = inspect.signature(SqliteStore)

    assert tuple(signature.parameters) == (
        "database_path",
    )
    assert (
        signature.parameters["database_path"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )


@pytest.mark.parametrize(
    "invalid_path",
    (
        None,
        object(),
        1,
        (),
    ),
)
def test_database_path_rejects_invalid_type(
    invalid_path: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="database_path must be a string or Path",
    ):
        SqliteStore(database_path=invalid_path)


def test_database_path_rejects_empty_string() -> None:
    with pytest.raises(
        ValueError,
        match="database_path must not be empty",
    ):
        SqliteStore(database_path="")


def test_constructor_creates_database_and_schema(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "publication.sqlite3"

    SqliteStore(database_path=database_path)

    assert database_path.is_file()

    with sqlite3.connect(database_path) as connection:
        table = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = ?
            """,
            (TABLE,),
        ).fetchone()

    assert table == (TABLE,)


def test_database_uses_wal_mode(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "publication.sqlite3"

    SqliteStore(database_path=database_path)

    with sqlite3.connect(database_path) as connection:
        journal_mode = connection.execute(
            "PRAGMA journal_mode"
        ).fetchone()[0]

    assert journal_mode.lower() == "wal"


def test_schema_stores_revision_as_text(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "publication.sqlite3"

    SqliteStore(database_path=database_path)

    with sqlite3.connect(database_path) as connection:
        columns = connection.execute(
            f"PRAGMA table_info({TABLE})"
        ).fetchall()

    declared_types = {
        row[1]: row[2]
        for row in columns
    }

    assert declared_types["revision"] == "TEXT"
    assert declared_types["signature"] == "BLOB"


def test_missing_read_returns_none(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)

    assert store.read(
        publication_id="publication-missing",
    ) is None


def test_create_and_read_round_trip_is_exact(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)
    state = create_state(
        publication_id="publication-001",
        scalar=7,
        phase=Phase.INTENT_RECORDED,
        revision=1,
    )

    assert store.create(state=state) is True

    restored = store.read(
        publication_id="publication-001",
    )

    assert restored == state
    assert restored is not state


@pytest.mark.parametrize("phase", tuple(Phase))
def test_create_and_read_preserves_every_phase(
    tmp_path: Path,
    phase: Phase,
) -> None:
    store = create_store(
        tmp_path,
        name=f"{phase.value}.sqlite3",
    )
    state = create_state(
        phase=phase,
    )

    assert store.create(state=state) is True
    assert store.read(
        publication_id="publication-001",
    ) == state


@pytest.mark.parametrize(
    "revision",
    (
        1,
        2,
        7,
        65537,
        (1 << 63) - 1,
        1 << 63,
        UINT64_MAX,
    ),
)
def test_full_uint64_revision_round_trip(
    tmp_path: Path,
    revision: int,
) -> None:
    store = create_store(
        tmp_path,
        name=f"revision-{revision}.sqlite3",
    )
    state = create_state(
        revision=revision,
    )

    assert store.create(state=state) is True
    assert store.read(
        publication_id="publication-001",
    ) == state


@pytest.mark.parametrize(
    "revision,encoded",
    (
        (1, "00000000000000000001"),
        (
            (1 << 63) - 1,
            "09223372036854775807",
        ),
        (
            1 << 63,
            "09223372036854775808",
        ),
        (
            UINT64_MAX,
            "18446744073709551615",
        ),
    ),
)
def test_revision_has_exact_twenty_digit_encoding(
    tmp_path: Path,
    revision: int,
    encoded: str,
) -> None:
    database_path = (
        tmp_path / f"encoding-{revision}.sqlite3"
    )
    store = SqliteStore(database_path=database_path)

    assert store.create(
        state=create_state(revision=revision)
    )

    with sqlite3.connect(database_path) as connection:
        stored_revision, storage_type = (
            connection.execute(
                f"""
                SELECT revision, typeof(revision)
                FROM {TABLE}
                WHERE publication_id = ?
                """,
                ("publication-001",),
            ).fetchone()
        )

    assert stored_revision == encoded
    assert storage_type == "text"


def test_duplicate_create_returns_false_and_preserves_original(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)
    original = create_state(
        scalar=1,
    )
    conflicting = create_state(
        scalar=7,
    )

    assert store.create(state=original) is True
    assert store.create(state=conflicting) is False
    assert store.read(
        publication_id="publication-001",
    ) == original


def test_distinct_publication_ids_are_independent(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)
    first = create_state(
        publication_id="publication-001",
        scalar=1,
    )
    second = create_state(
        publication_id="publication-002",
        scalar=2,
    )

    assert store.create(state=first)
    assert store.create(state=second)
    assert store.read(
        publication_id="publication-001",
    ) == first
    assert store.read(
        publication_id="publication-002",
    ) == second


def test_state_persists_across_store_instances(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "publication.sqlite3"
    state = create_state()

    first_store = SqliteStore(
        database_path=database_path,
    )
    assert first_store.create(state=state)

    second_store = SqliteStore(
        database_path=database_path,
    )

    assert second_store.read(
        publication_id="publication-001",
    ) == state


def test_compare_and_swap_updates_once(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)
    current = create_state(
        phase=Phase.INTENT_RECORDED,
        revision=1,
    )
    next_state = transition(
        current_state=current,
        target_phase=Phase.PREPARED,
    )

    assert store.create(state=current)
    assert store.compare_and_swap(
        expected_revision=1,
        next_state=next_state,
    ) is True
    assert store.read(
        publication_id="publication-001",
    ) == next_state


def test_stale_compare_and_swap_returns_false(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)
    current = create_state()
    prepared = transition(
        current_state=current,
        target_phase=Phase.PREPARED,
    )
    aborted_decision = transition(
        current_state=current,
        target_phase=Phase.ABORT_DECIDED,
    )

    assert store.create(state=current)
    assert store.compare_and_swap(
        expected_revision=1,
        next_state=prepared,
    )
    assert store.compare_and_swap(
        expected_revision=1,
        next_state=aborted_decision,
    ) is False
    assert store.read(
        publication_id="publication-001",
    ) == prepared


def test_two_concurrent_cas_writers_have_one_winner(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "publication.sqlite3"
    first_store = SqliteStore(
        database_path=database_path,
    )
    second_store = SqliteStore(
        database_path=database_path,
    )
    current = create_state()
    prepared = transition(
        current_state=current,
        target_phase=Phase.PREPARED,
    )
    abort_decided = transition(
        current_state=current,
        target_phase=Phase.ABORT_DECIDED,
    )

    assert first_store.create(state=current)

    def write_prepared() -> bool:
        return first_store.compare_and_swap(
            expected_revision=1,
            next_state=prepared,
        )

    def write_abort() -> bool:
        return second_store.compare_and_swap(
            expected_revision=1,
            next_state=abort_decided,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = tuple(
            executor.map(
                lambda operation: operation(),
                (
                    write_prepared,
                    write_abort,
                ),
            )
        )

    assert sorted(results) == [False, True]

    retained = first_store.read(
        publication_id="publication-001",
    )
    assert retained in (
        prepared,
        abort_decided,
    )
    assert retained.revision == 2


def test_cas_rejects_changed_cryptographic_identity(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)
    current = create_state(
        scalar=1,
    )
    changed = create_state(
        scalar=7,
        phase=Phase.PREPARED,
        revision=2,
    )

    assert store.create(state=current)
    assert store.compare_and_swap(
        expected_revision=1,
        next_state=changed,
    ) is False
    assert store.read(
        publication_id="publication-001",
    ) == current


def test_cas_rejects_different_publication_id(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)
    current = create_state(
        publication_id="publication-001",
    )
    changed = create_state(
        publication_id="publication-002",
        phase=Phase.PREPARED,
        revision=2,
    )

    assert store.create(state=current)
    assert store.compare_and_swap(
        expected_revision=1,
        next_state=changed,
    ) is False
    assert store.read(
        publication_id="publication-001",
    ) == current


@pytest.mark.parametrize(
    "expected_revision,next_revision",
    (
        (1, 1),
        (1, 3),
        (7, 9),
        ((1 << 63), (1 << 63) + 2),
    ),
)
def test_cas_requires_exact_successor_revision(
    tmp_path: Path,
    expected_revision: int,
    next_revision: int,
) -> None:
    store = create_store(tmp_path)
    next_state = create_state(
        phase=Phase.PREPARED,
        revision=next_revision,
    )

    with pytest.raises(
        ValueError,
        match=(
            "next_state revision must be the exact "
            "successor of expected_revision"
        ),
    ):
        store.compare_and_swap(
            expected_revision=expected_revision,
            next_state=next_state,
        )


@pytest.mark.parametrize(
    "invalid_revision",
    (
        None,
        True,
        False,
        1.0,
        "1",
        0,
        -1,
        UINT64_MAX + 1,
    ),
)
def test_cas_validates_expected_revision(
    tmp_path: Path,
    invalid_revision: object,
) -> None:
    store = create_store(tmp_path)
    next_state = create_state(
        phase=Phase.PREPARED,
        revision=2,
    )

    with pytest.raises((TypeError, ValueError)):
        store.compare_and_swap(
            expected_revision=invalid_revision,
            next_state=next_state,
        )


@pytest.mark.parametrize(
    "invalid_state",
    (
        None,
        object(),
        "state",
        1,
        (),
    ),
)
def test_create_rejects_invalid_state(
    tmp_path: Path,
    invalid_state: object,
) -> None:
    store = create_store(tmp_path)

    with pytest.raises(
        TypeError,
        match="state must be a",
    ):
        store.create(state=invalid_state)


@pytest.mark.parametrize(
    "invalid_state",
    (
        None,
        object(),
        "state",
        1,
        (),
    ),
)
def test_cas_rejects_invalid_next_state(
    tmp_path: Path,
    invalid_state: object,
) -> None:
    store = create_store(tmp_path)

    with pytest.raises(
        TypeError,
        match="next_state must be a",
    ):
        store.compare_and_swap(
            expected_revision=1,
            next_state=invalid_state,
        )


@pytest.mark.parametrize(
    "invalid_id",
    (
        None,
        object(),
        1,
        b"publication-001",
        (),
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
        store.read(publication_id=invalid_id)


def test_read_rejects_empty_publication_id(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)

    with pytest.raises(
        ValueError,
        match="publication_id must not be empty",
    ):
        store.read(publication_id="")


def test_publication_id_is_parameterized_not_executed(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)
    malicious_id = (
        "publication-001'; DROP TABLE "
        f"{TABLE}; --"
    )
    state = create_state(
        publication_id=malicious_id,
    )

    assert store.create(state=state)
    assert store.read(
        publication_id=malicious_id,
    ) == state

    with sqlite3.connect(
        tmp_path / "publication.sqlite3"
    ) as connection:
        table = connection.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type = 'table' AND name = ?
            """,
            (TABLE,),
        ).fetchone()

    assert table == (TABLE,)


def test_noncanonical_stored_revision_fails_closed(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "publication.sqlite3"
    store = SqliteStore(
        database_path=database_path,
    )
    assert store.create(state=create_state())

    with sqlite3.connect(database_path) as connection:
        connection.execute(
            "PRAGMA ignore_check_constraints=ON"
        )
        connection.execute(
            f"""
            UPDATE {TABLE}
            SET revision = ?
            WHERE publication_id = ?
            """,
            (
                "1",
                "publication-001",
            ),
        )

    with pytest.raises(
        ValueError,
        match="stored revision is not canonical",
    ):
        store.read(
            publication_id="publication-001",
        )


def test_noncanonical_checkpoint_fails_closed_on_read(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "publication.sqlite3"
    store = SqliteStore(
        database_path=database_path,
    )
    assert store.create(state=create_state())

    with sqlite3.connect(database_path) as connection:
        serialized = connection.execute(
            f"""
            SELECT checkpoint_serialization
            FROM {TABLE}
            WHERE publication_id = ?
            """,
            ("publication-001",),
        ).fetchone()[0]
        connection.execute(
            f"""
            UPDATE {TABLE}
            SET checkpoint_serialization = ?
            WHERE publication_id = ?
            """,
            (
                serialized.replace(
                    ',"origin"',
                    ', "origin"',
                    1,
                ),
                "publication-001",
            ),
        )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint_serialization must be canonical"
        ),
    ):
        store.read(
            publication_id="publication-001",
        )


def test_application_composes_with_sqlite_store(
    tmp_path: Path,
) -> None:
    store = create_store(tmp_path)
    current = create_state()

    assert store.create(state=current)

    next_state = apply_transition(
        state_store=store,
        publication_id="publication-001",
        expected_revision=1,
        target_phase=Phase.PREPARED,
    )

    assert next_state.phase is Phase.PREPARED
    assert next_state.revision == 2
    assert store.read(
        publication_id="publication-001",
    ) == next_state


def test_adapter_uses_no_pickle(
    tmp_path: Path,
) -> None:
    create_store(tmp_path)

    source = inspect.getsource(SqliteStore).lower()

    assert "pickle" not in source
    assert "eval(" not in source
    assert "exec(" not in source
