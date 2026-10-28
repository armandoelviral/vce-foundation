import sqlite3
from collections.abc import Callable
from pathlib import Path

from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
    ValidatedCaseAccessContext,
)
from sp001.contracts.retail_inspection_observation import (
    RetailInspectionObservation,
)
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict,
    RetailInspectionObservationIdentity,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
    deserialize_retail_inspection_observation as deserialize,
)
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.infrastructure.sqlite_retail_inspection_observations import (
    SqliteRetailInspectionObservationStore,
)
from sp001.services.retail_observation_access_policy import (
    required_retail_observation_permissions,
    token_allows_retail_observation,
)


class InspectionObservationAuthenticationRejected(PermissionError):
    """The supplied authenticated context is no longer usable."""


class InspectionObservationAccessDenied(PermissionError):
    """The exact operation and case are not authorized."""


class SqliteAuthorizedInspectionObservations:
    """Trusted backend capability: caller must supply authenticated context.

    Grants and observations use one database and transaction.
    Does not authenticate credentials or verify declared observer attribution.
    Read revocation after snapshot establishment applies to the next query.
    """

    def __init__(
        self, *, database_path: str | Path,
        expected_audience: str, clock: Callable[[], int],
    ) -> None:
        if not isinstance(database_path, (str, Path)):
            raise TypeError("database_path must be a string or Path")
        if not str(database_path).strip() or str(database_path) == ":memory:":
            raise ValueError("database_path must identify a file")
        if not isinstance(expected_audience, str):
            raise TypeError("expected_audience must be a string")
        if not expected_audience.strip():
            raise ValueError("expected_audience must not be empty")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._path = str(database_path)
        self._audience = expected_audience
        self._clock = clock
        SqliteCaseAccessGrants(database_path=database_path)
        SqliteRetailInspectionObservationStore(database_path=database_path)

    def _connect(self):
        connection = sqlite3.connect(
            self._path, timeout=5, isolation_level=None,
        )
        try:
            connection.execute("PRAGMA synchronous=FULL")
        except BaseException:
            connection.close()
            raise
        return connection

    def _authorize(self, connection, access, case_id, operation):
        now = self._clock()
        if type(now) is not int:
            raise TypeError("clock must return integer Unix seconds")
        if now < 0:
            raise ValueError("clock must return nonnegative Unix seconds")
        if (
            access.audience != self._audience
            or not access.issued_at <= access.not_before <= now < access.expires_at
        ):
            raise InspectionObservationAuthenticationRejected(
                "access context unusable"
            )
        if not token_allows_retail_observation(
            access=access, case_id=case_id, operation=operation,
            expected_audience=self._audience, at_time=now,
        ):
            raise InspectionObservationAccessDenied("observation access denied")
        for permission in required_retail_observation_permissions(
            case_id=case_id, operation=operation,
        ):
            row = connection.execute("""
                SELECT 1 FROM case_access_grants
                WHERE issuer=? AND subject=? AND case_id=? AND operation=?
                  AND revoked=0 AND valid_from<=? AND expires_at>?
                LIMIT 1
            """, (
                access.principal.issuer, access.principal.subject,
                permission.case_id, permission.operation.value, now, now,
            )).fetchone()
            if row is None:
                raise InspectionObservationAccessDenied(
                    "observation access denied"
                )

    @staticmethod
    def _rollback(connection, error):
        if connection.in_transaction:
            try:
                connection.execute("ROLLBACK")
            except BaseException as rollback_error:
                error.add_note(
                    "Rollback also failed: " + type(rollback_error).__name__
                )

    def save_authorized(self, *, access, observation):
        if not isinstance(access, ValidatedCaseAccessContext):
            raise TypeError("access must be a ValidatedCaseAccessContext")
        if type(observation) is not RetailInspectionObservation:
            raise TypeError("observation must be a RetailInspectionObservation")
        document = serialize(observation)
        validated = deserialize(document)
        if validated != observation:
            raise ValueError("serialized observation differs")
        key = (
            observation.observation_id, str(observation.observation_version),
        )
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            self._authorize(
                connection, access, observation.case_id,
                Operation.SAVE_RETAIL_OBSERVATION,
            )
            row = connection.execute("""
                SELECT document FROM retail_inspection_observations
                WHERE observation_id=? AND observation_version=?
            """, key).fetchone()
            if row is not None:
                if row[0] != document:
                    raise RetailInspectionObservationConflict(
                        "observation identity/version has a different document"
                    )
            else:
                connection.execute("""
                    INSERT INTO retail_inspection_observations
                        (observation_id, observation_version, document)
                    VALUES (?, ?, ?)
                """, (*key, document))
            self._authorize(
                connection, access, observation.case_id,
                Operation.SAVE_RETAIL_OBSERVATION,
            )
            connection.execute("COMMIT")
            return validated
        except BaseException as error:
            self._rollback(connection, error)
            raise
        finally:
            connection.close()

    def recover_authorized(self, *, access, identity, case_id):
        if not isinstance(access, ValidatedCaseAccessContext):
            raise TypeError("access must be a ValidatedCaseAccessContext")
        if type(identity) is not RetailInspectionObservationIdentity:
            raise TypeError("identity must be an observation identity")
        required_retail_observation_permissions(
            case_id=case_id, operation=Operation.READ_RETAIL_OBSERVATION,
        )
        connection = self._connect()
        try:
            connection.execute("BEGIN")
            self._authorize(
                connection, access, case_id, Operation.READ_RETAIL_OBSERVATION,
            )
            row = connection.execute("""
                SELECT document FROM retail_inspection_observations
                WHERE observation_id=? AND observation_version=?
            """, (
                identity.observation_id, str(identity.observation_version),
            )).fetchone()
            observation = None if row is None else deserialize(row[0])
            if observation is not None:
                if (
                    observation.observation_id != identity.observation_id
                    or observation.observation_version
                    != identity.observation_version
                ):
                    raise ValueError("document identity/version mismatch")
                if observation.case_id != case_id:
                    raise InspectionObservationAccessDenied(
                        "observation access denied"
                    )
            self._authorize(
                connection, access, case_id, Operation.READ_RETAIL_OBSERVATION,
            )
            connection.execute("COMMIT")
            return observation
        except BaseException as error:
            self._rollback(connection, error)
            raise
        finally:
            connection.close()
