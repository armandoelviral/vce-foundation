from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
    ValidatedCaseAccessContext,
)
from sp001.contracts.retail_observation_operation import (
    RetailObservationSaveRequest as Request,
    RetailObservationOperationIdentity as Identity,
    RetailObservationOperationReceipt as Receipt,
    RetailObservationEffectDisposition as Disposition,
    RetailObservationOperationConflict,
)
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationIdentity,
    StoredRetailInspectionObservation,
    RetailInspectionObservationConflict,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    SqliteAuthorizedInspectionObservations,
)
from sp001.services.retail_observation_operation_validation import (
    validate_retail_observation_operation as validate,
)


class SqliteObservationOperations(SqliteAuthorizedInspectionObservations):
    """Trusted backend: caller supplies an authenticated access context.

    Saves effect and receipt in one local transaction. Does not authenticate,
    provide OS isolation, attest physical durability, or verify observer identity.
    The stored principal identifies the accepted operation, not inspection
    authorship. Existing save_authorized remains the legacy receipt-free path.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        connection = self._connect()
        try:
            self._require_profile(connection)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS retail_observation_operations (
                    issuer TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    case_id TEXT NOT NULL,
                    request_id TEXT NOT NULL,
                    observation_id TEXT NOT NULL,
                    observation_version TEXT NOT NULL,
                    document TEXT NOT NULL,
                    disposition TEXT NOT NULL
                        CHECK(disposition IN ('CREATED', 'REUSED')),
                    PRIMARY KEY (issuer, subject, case_id, request_id)
                )
            """)
        finally:
            connection.close()

    @staticmethod
    def _require_profile(connection):
        mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
        synchronous = connection.execute("PRAGMA synchronous").fetchone()[0]
        if mode.lower() != "wal" or synchronous != 2:
            raise RuntimeError("operation requires WAL and synchronous=FULL")

    @staticmethod
    def _stored(item, document):
        return StoredRetailInspectionObservation(
            RetailInspectionObservationIdentity(
                item.observation_id, item.observation_version,
            ),
            document,
        )

    def save_operation_authorized(self, *, access, request):
        if type(access) is not ValidatedCaseAccessContext:
            raise TypeError("access must be a validated access context")
        if type(request) is not Request:
            raise TypeError("request must be an observation save request")

        item = request.observation
        document = serialize(item)
        operation = Identity(
            access.principal, item.case_id, request.request_id,
        )
        operation_key = (
            operation.principal.issuer, operation.principal.subject,
            operation.case_id, operation.request_id,
        )
        observation_key = (item.observation_id, str(item.observation_version))
        connection = self._connect()
        try:
            self._require_profile(connection)
            connection.execute("BEGIN IMMEDIATE")
            self._authorize(
                connection, access, item.case_id,
                Operation.SAVE_RETAIL_OBSERVATION,
            )

            previous = connection.execute("""
                SELECT observation_id, observation_version, document, disposition
                FROM retail_observation_operations
                WHERE issuer=? AND subject=? AND case_id=? AND request_id=?
            """, operation_key).fetchone()

            existing = connection.execute("""
                SELECT document FROM retail_inspection_observations
                WHERE observation_id=? AND observation_version=?
            """, observation_key).fetchone()

            if previous is not None:
                stored = StoredRetailInspectionObservation(
                    RetailInspectionObservationIdentity(
                        previous[0], int(previous[1]),
                    ),
                    previous[2],
                )
                receipt = Receipt(
                    operation, stored, Disposition(previous[3]),
                )
                # Validate historical evidence before considering new intent.
                from sp001.infrastructure.retail_inspection_observation_serialization import (
                    deserialize_retail_inspection_observation as deserialize,
                )
                historical = deserialize(stored.document)
                validate(
                    request=Request(request.request_id, historical),
                    receipt=receipt, principal=access.principal,
                )
                if (
                    previous[0] != item.observation_id
                    or previous[1] != str(item.observation_version)
                    or previous[2] != document
                ):
                    raise RetailObservationOperationConflict(
                        "operation identity has different intent"
                    )
                if existing is None or existing[0] != stored.document:
                    raise ValueError("receipt and persisted effect disagree")
            else:
                if existing is None:
                    connection.execute("""
                        INSERT INTO retail_inspection_observations
                            (observation_id, observation_version, document)
                        VALUES (?, ?, ?)
                    """, (*observation_key, document))
                    disposition = Disposition.CREATED
                else:
                    if existing[0] != document:
                        raise RetailInspectionObservationConflict(
                            "observation identity/version has different content"
                        )
                    disposition = Disposition.REUSED

                receipt = Receipt(
                    operation, self._stored(item, document), disposition,
                )
                validate(
                    request=request, receipt=receipt, principal=access.principal,
                )
                connection.execute("""
                    INSERT INTO retail_observation_operations
                        (issuer, subject, case_id, request_id,
                         observation_id, observation_version, document,
                         disposition)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    *operation_key, *observation_key, document, disposition.value,
                ))

            validate(
                request=request, receipt=receipt, principal=access.principal,
            )
            self._authorize(
                connection, access, item.case_id,
                Operation.SAVE_RETAIL_OBSERVATION,
            )
            connection.execute("COMMIT")
            return receipt
        except BaseException as error:
            self._rollback(connection, error)
            raise
        finally:
            connection.close()
