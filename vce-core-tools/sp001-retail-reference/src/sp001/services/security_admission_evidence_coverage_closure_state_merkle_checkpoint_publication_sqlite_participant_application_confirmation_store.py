import sqlite3
from pathlib import Path

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_parsing import (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)


Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)
ConfirmationStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore
)

_TABLE_NAME = (
    "security_admission_merkle_checkpoint_publication_"
    "participant_application_confirmations"
)
_CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (
    publication_id TEXT NOT NULL,
    participant_id TEXT NOT NULL,
    confirmation_serialization TEXT NOT NULL,
    PRIMARY KEY (publication_id, participant_id)
) STRICT
"""
_SELECT_CONFIRMATIONS = f"""
SELECT participant_id, confirmation_serialization
FROM {_TABLE_NAME}
WHERE publication_id = ?
ORDER BY participant_id ASC
"""
_INSERT_CONFIRMATION = f"""
INSERT OR IGNORE INTO {_TABLE_NAME} (
    publication_id,
    participant_id,
    confirmation_serialization
) VALUES (?, ?, ?)
"""


class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteParticipantApplicationConfirmationStore:
    """Persist canonical participant application confirmations once in SQLite."""

    __slots__ = (
        "_database_path",
    )

    def __init__(
        self,
        *,
        database_path: str | Path,
    ) -> None:
        if not isinstance(database_path, (str, Path)):
            raise TypeError(
                "database_path must be a string or pathlib.Path"
            )
        if isinstance(database_path, str) and not database_path:
            raise ValueError(
                "database_path must not be empty"
            )

        self._database_path = str(database_path)

        with self._connect() as connection:
            connection.execute(_CREATE_TABLE)

    def read(
        self,
        *,
        publication_id: str,
    ) -> ConfirmationSet:
        """Read canonical durable confirmations for one publication."""

        self._validate_publication_id(
            publication_id=publication_id,
        )

        with self._connect() as connection:
            rows = connection.execute(
                _SELECT_CONFIRMATIONS,
                (publication_id,),
            ).fetchall()

        confirmations: list[Confirmation] = []

        for row in rows:
            if (
                type(row) is not tuple
                or len(row) != 2
                or type(row[0]) is not str
                or type(row[1]) is not str
            ):
                raise ValueError(
                    "stored application confirmation row is invalid"
                )

            retained_participant_id = row[0]
            stored_confirmation = (
                parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
                    serialization=row[1],
                )
            )

            if (
                stored_confirmation.participant_id
                != retained_participant_id
            ):
                raise ValueError(
                    "stored application confirmation has a "
                    "different participant_id"
                )

            if (
                stored_confirmation
                .publication_state
                .publication_id
                != publication_id
            ):
                raise ValueError(
                    "stored application confirmation has a "
                    "different publication_id"
                )

            confirmation = (
                deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
                    stored_confirmation=stored_confirmation,
                )
            )

            if (
                confirmation.participant_id
                != retained_participant_id
            ):
                raise ValueError(
                    "deserialized application confirmation has a "
                    "different participant_id"
                )

            retained_publication_id = (
                confirmation
                .publication_state
                .publication_intent
                .publication_id
            )
            if retained_publication_id != publication_id:
                raise ValueError(
                    "deserialized application confirmation has a "
                    "different publication_id"
                )

            confirmations.append(confirmation)

        return ConfirmationSet(
            confirmations=tuple(confirmations),
        )

    def create(
        self,
        *,
        confirmation: Confirmation,
    ) -> bool:
        """Append once; return False when the participant already exists."""

        if not isinstance(
            confirmation,
            Confirmation,
        ):
            raise TypeError(
                "confirmation must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationParticipant"
                "ApplicationConfirmation"
            )

        publication_id = (
            confirmation
            .publication_state
            .publication_intent
            .publication_id
        )
        participant_id = confirmation.participant_id

        stored_confirmation = (
            project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
                confirmation=confirmation,
            )
        )
        serialization = (
            serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
                stored_confirmation=stored_confirmation,
            )
        )

        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            cursor = connection.execute(
                _INSERT_CONFIRMATION,
                (
                    publication_id,
                    participant_id,
                    serialization,
                ),
            )
            created = cursor.rowcount == 1
            connection.execute("COMMIT")
        except BaseException:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            raise
        finally:
            connection.close()

        return created

    @staticmethod
    def _validate_publication_id(
        *,
        publication_id: str,
    ) -> None:
        if type(publication_id) is not str:
            raise TypeError(
                "publication_id must be a string"
            )
        if not publication_id:
            raise ValueError(
                "publication_id must not be empty"
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self._database_path,
            timeout=30.0,
            isolation_level=None,
        )
        connection.execute(
            "PRAGMA foreign_keys=ON"
        )
        connection.execute(
            "PRAGMA synchronous=FULL"
        )
        connection.execute(
            "PRAGMA busy_timeout=30000"
        )
        connection.execute(
            "PRAGMA journal_mode=WAL"
        )
        return connection


assert issubclass(
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteParticipantApplicationConfirmationStore,
    object,
)
