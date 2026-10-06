from contextlib import closing
from pathlib import Path
import sqlite3

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)
StoredState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState
)

_TABLE = "security_admission_checkpoint_publication_state"
_REVISION_WIDTH = 20

_SELECT_COLUMNS = """
    storage_schema_version,
    publication_id,
    checkpoint_serialization,
    signing_key_id,
    signing_algorithm,
    public_key_encoding,
    public_key_fingerprint,
    signature_encoding,
    signature,
    phase,
    revision
"""

_CREATE_SCHEMA = f"""
CREATE TABLE IF NOT EXISTS {_TABLE} (
    publication_id TEXT PRIMARY KEY NOT NULL,
    storage_schema_version INTEGER NOT NULL
        CHECK (storage_schema_version = 1),
    checkpoint_serialization TEXT NOT NULL,
    signing_key_id TEXT NOT NULL,
    signing_algorithm TEXT NOT NULL,
    public_key_encoding TEXT NOT NULL,
    public_key_fingerprint TEXT NOT NULL,
    signature_encoding TEXT NOT NULL,
    signature BLOB NOT NULL,
    phase TEXT NOT NULL CHECK (
        phase IN (
            'INTENT_RECORDED',
            'PREPARED',
            'COMMIT_DECIDED',
            'COMMITTED',
            'ABORT_DECIDED',
            'ABORTED'
        )
    ),
    revision TEXT NOT NULL CHECK (
        length(revision) = 20
        AND revision NOT GLOB '*[^0-9]*'
    )
) WITHOUT ROWID
"""

_INSERT = f"""
INSERT OR IGNORE INTO {_TABLE} (
    publication_id,
    storage_schema_version,
    checkpoint_serialization,
    signing_key_id,
    signing_algorithm,
    public_key_encoding,
    public_key_fingerprint,
    signature_encoding,
    signature,
    phase,
    revision
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_SELECT = f"""
SELECT {_SELECT_COLUMNS}
FROM {_TABLE}
WHERE publication_id = ?
"""

_COMPARE_AND_SWAP = f"""
UPDATE {_TABLE}
SET
    phase = ?,
    revision = ?
WHERE
    publication_id = ?
    AND revision = ?
    AND storage_schema_version = ?
    AND checkpoint_serialization = ?
    AND signing_key_id = ?
    AND signing_algorithm = ?
    AND public_key_encoding = ?
    AND public_key_fingerprint = ?
    AND signature_encoding = ?
    AND signature = ?
"""


class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteStateStore:
    """SQLite WAL adapter with atomic optimistic concurrency."""

    def __init__(
        self,
        *,
        database_path: str | Path,
    ) -> None:
        if not isinstance(database_path, (str, Path)):
            raise TypeError(
                "database_path must be a string or Path"
            )
        if not str(database_path):
            raise ValueError(
                "database_path must not be empty"
            )

        self._database_path = Path(database_path)
        self._initialize()

    def read(
        self,
        *,
        publication_id: str,
    ) -> PublicationState | None:
        _validate_publication_id(publication_id)

        with closing(self._connect()) as connection:
            row = connection.execute(
                _SELECT,
                (publication_id,),
            ).fetchone()

        if row is None:
            return None

        stored_state = _stored_state_from_row(row)

        return deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state(
            stored_state=stored_state,
        )

    def create(
        self,
        *,
        state: PublicationState,
    ) -> bool:
        if not isinstance(state, PublicationState):
            raise TypeError(
                "state must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationState"
            )

        stored = (
            project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state(
                state=state,
            )
        )

        with closing(self._connect()) as connection:
            with connection:
                cursor = connection.execute(
                    _INSERT,
                    _insert_values(stored),
                )

        return cursor.rowcount == 1

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state: PublicationState,
    ) -> bool:
        validate_security_admission_positive_uint64(
            value=expected_revision,
            field="expected_revision",
        )
        if not isinstance(next_state, PublicationState):
            raise TypeError(
                "next_state must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationState"
            )
        if next_state.revision != expected_revision + 1:
            raise ValueError(
                "next_state revision must be the exact "
                "successor of expected_revision"
            )

        stored = (
            project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state(
                state=next_state,
            )
        )

        values = (
            stored.phase,
            _encode_revision(stored.revision),
            stored.publication_id,
            _encode_revision(expected_revision),
            stored.storage_schema_version,
            stored.checkpoint_serialization,
            stored.signing_key_id,
            stored.signing_algorithm,
            stored.public_key_encoding,
            stored.public_key_fingerprint,
            stored.signature_encoding,
            stored.signature,
        )

        with closing(self._connect()) as connection:
            with connection:
                cursor = connection.execute(
                    _COMPARE_AND_SWAP,
                    values,
                )

        return cursor.rowcount == 1

    def _initialize(self) -> None:
        with closing(self._connect()) as connection:
            journal_mode = connection.execute(
                "PRAGMA journal_mode=WAL"
            ).fetchone()[0]
            if str(journal_mode).lower() != "wal":
                raise RuntimeError(
                    "SQLite journal mode must be WAL"
                )

            with connection:
                connection.execute(_CREATE_SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self._database_path,
            timeout=5.0,
        )
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA synchronous=FULL")
        return connection


def _validate_publication_id(
    publication_id: object,
) -> None:
    if type(publication_id) is not str:
        raise TypeError("publication_id must be a string")
    if not publication_id:
        raise ValueError("publication_id must not be empty")


def _encode_revision(
    revision: int,
) -> str:
    validate_security_admission_positive_uint64(
        value=revision,
        field="revision",
    )
    return f"{revision:0{_REVISION_WIDTH}d}"


def _decode_revision(
    value: object,
) -> int:
    if (
        type(value) is not str
        or len(value) != _REVISION_WIDTH
        or not value.isascii()
        or not value.isdecimal()
    ):
        raise ValueError(
            "stored revision is not canonical"
        )

    revision = int(value)
    if _encode_revision(revision) != value:
        raise ValueError(
            "stored revision is not canonical"
        )

    return revision


def _insert_values(
    stored: StoredState,
) -> tuple[object, ...]:
    return (
        stored.publication_id,
        stored.storage_schema_version,
        stored.checkpoint_serialization,
        stored.signing_key_id,
        stored.signing_algorithm,
        stored.public_key_encoding,
        stored.public_key_fingerprint,
        stored.signature_encoding,
        stored.signature,
        stored.phase,
        _encode_revision(stored.revision),
    )


def _stored_state_from_row(
    row: tuple[object, ...],
) -> StoredState:
    if len(row) != 11:
        raise ValueError(
            "stored publication row has invalid cardinality"
        )

    return StoredState(
        storage_schema_version=row[0],
        publication_id=row[1],
        checkpoint_serialization=row[2],
        signing_key_id=row[3],
        signing_algorithm=row[4],
        public_key_encoding=row[5],
        public_key_fingerprint=row[6],
        signature_encoding=row[7],
        signature=row[8],
        phase=row[9],
        revision=_decode_revision(row[10]),
    )
