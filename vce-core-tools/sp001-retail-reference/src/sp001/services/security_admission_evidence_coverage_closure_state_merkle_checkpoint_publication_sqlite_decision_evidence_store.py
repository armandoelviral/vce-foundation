import sqlite3
from pathlib import Path

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_parsing import (
    parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
)


DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
DecisionRecordStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore
)
ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)

_TABLE_NAME = (
    "security_admission_merkle_checkpoint_publication_decision_evidence"
)
_CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (
    publication_id TEXT PRIMARY KEY NOT NULL,
    evidence_serialization TEXT NOT NULL
) STRICT
"""
_SELECT_EVIDENCE = f"""
SELECT evidence_serialization
FROM {_TABLE_NAME}
WHERE publication_id = ?
"""
_INSERT_EVIDENCE = f"""
INSERT OR IGNORE INTO {_TABLE_NAME} (
    publication_id,
    evidence_serialization
) VALUES (?, ?)
"""


class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore:
    """Persist complete signed publication-decision evidence once in SQLite."""

    __slots__ = (
        "_database_path",
        "_participant_set",
    )

    def __init__(
        self,
        *,
        database_path: str | Path,
        participant_set: ParticipantSet,
    ) -> None:
        if not isinstance(database_path, (str, Path)):
            raise TypeError(
                "database_path must be a string or pathlib.Path"
            )
        if isinstance(database_path, str) and not database_path:
            raise ValueError(
                "database_path must not be empty"
            )
        if not isinstance(participant_set, ParticipantSet):
            raise TypeError(
                "participant_set must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationParticipantSet"
            )

        self._database_path = str(database_path)
        self._participant_set = participant_set

        with self._connect() as connection:
            connection.execute(_CREATE_TABLE)

    def read(
        self,
        *,
        publication_id: str,
    ) -> DecisionRecord | None:
        """Read and rederive one complete append-only publication decision."""

        if type(publication_id) is not str:
            raise TypeError(
                "publication_id must be a string"
            )
        if not publication_id:
            raise ValueError(
                "publication_id must not be empty"
            )

        with self._connect() as connection:
            row = connection.execute(
                _SELECT_EVIDENCE,
                (publication_id,),
            ).fetchone()

        if row is None:
            return None
        if (
            type(row) is not tuple
            or len(row) != 1
            or type(row[0]) is not str
        ):
            raise ValueError(
                "stored decision evidence row is invalid"
            )

        stored_evidence = (
            parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
                serialization=row[0],
            )
        )
        if (
            stored_evidence
            .publication_intent
            .publication_id
            != publication_id
        ):
            raise ValueError(
                "stored decision evidence has a different publication_id"
            )

        decision_record = (
            deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
                stored_evidence=stored_evidence,
                participant_set=self._participant_set,
            )
        )
        retained_publication_id = (
            decision_record
            .publication_intent
            .publication_id
        )
        if retained_publication_id != publication_id:
            raise ValueError(
                "deserialized decision record has a different publication_id"
            )

        return decision_record

    def create(
        self,
        *,
        decision_record: DecisionRecord,
    ) -> bool:
        """Append once; return False when publication_id already exists."""

        if not isinstance(
            decision_record,
            DecisionRecord,
        ):
            raise TypeError(
                "decision_record must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationDecisionRecord"
            )

        publication_id = (
            decision_record
            .publication_intent
            .publication_id
        )
        stored_evidence = (
            project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
                decision_record=decision_record,
            )
        )
        serialization = (
            serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
                stored_evidence=stored_evidence,
            )
        )

        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            cursor = connection.execute(
                _INSERT_EVIDENCE,
                (
                    publication_id,
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
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationSqliteDecisionEvidenceStore,
    object,
)
